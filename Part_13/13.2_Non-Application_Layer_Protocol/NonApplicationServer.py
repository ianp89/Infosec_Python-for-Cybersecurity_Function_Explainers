# This script uses scapy to sniff for ICMP packets, isolated exfiltrated data within those packets, and print them to the console.

from scapy.all import *

def printData(x):
    d = chr(x[ICMP].code)
    print(d,end="",flush=True)
# Isolates desired data hidden in ICMP packets, and prints.

sniff(filter="icmp", prn=printData)
# Prints sniffed ICMP packet data.
