#!/usr/bin/env python
import scapy.all as scapy
import argparse


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)  #create arp request
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  #broadcast MAC
    packet = broadcast / arp_request #combining frames
    # print(packet.show())
    ans_list, unans_list = scapy.srp(packet, timeout=1)
    client_list = []
    for i in ans_list:
        client_list.append({'ip': i[1].psrc,'mac':i[1].hwsrc})
    print_result(client_list)

def print_result(client_list):
    print("IP\t\t\t\tMAC\n--------------------------------------------------")
    for i in client_list:
        print(i['ip']+"\t\t\t"+i['mac'])


def get_arguments():
    parser=argparse.ArgumentParser()
    parser.add_argument("-i","--ip",dest="ip",help="IP to scan")
    option = parser.parse_args()
    return option
option = get_arguments()
scan(option.ip)
