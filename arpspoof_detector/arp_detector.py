import scapy.all as  scapy

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)  #create arp request
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  #broadcast MAC
    packet = broadcast / arp_request #combining frames
    # print(packet.show())
    ans_list = scapy.srp(packet, timeout=1, verbose=False)[0]
    mac_addr = ans_list[0][1].hwsrc
    return mac_addr

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def process_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac= get_mac(packet[scapy.ARP].psrc)
            response_mac=packet[scapy.ARP].hwsrc

            if real_mac!=response_mac:
                print('[+] You are under attack!')

        except IndexError:
            pass
sniff("eth0")