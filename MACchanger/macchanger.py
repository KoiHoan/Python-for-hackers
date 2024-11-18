#! /usr/bin/env python

import subprocess
import argparse
# import optparse
import re

def get_arguments():
    parser=argparse.ArgumentParser()
    parser.add_argument("-i","--interface",dest="interface",help="Interface to change its MAC address")
    parser.add_argument("-m","--mac",dest="mac",help="new MAC address")
    options= parser.parse_args()
    return options

def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface,"down"])
    subprocess.call(["ifconfig", interface,"hw","ether",new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    print(mac_result.group(0))
    # if mac_result:
    #     print(mac)

options_list = get_arguments()
change_mac(options_list.interface,options_list.mac)
get_current_mac(options_list.interface)



