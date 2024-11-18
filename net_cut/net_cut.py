#!usr/bin/env python
import netfilterqueue


def process_packet(packet):
    print(packet)
    # packet.accept()
    packet.drop()



#iptables -I FORWARD -j NFQUEUE  --queue-num 0
#execute in hacker machine to create a queue
queue = netfilterqueue.NetfilterQueue() #create instance
queue.bind(0, process_packet)
queue.run()# connect with the we create in hacker machine ,
                                # 0: number of queue, process_packet: callback whenever get packet in queue