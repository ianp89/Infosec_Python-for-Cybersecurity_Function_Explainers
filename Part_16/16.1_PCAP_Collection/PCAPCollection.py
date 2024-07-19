# This script captures traffic sent to decoy IP:Port destinations.

from scapy.all import *

decoys = {
    "127.0.0.1":[443,8443],
    "10.10.10.8":[443,8443]
}
# As per usual, these are only examples!

def analyzePackets(p):
    if p.haslayer(IP):
        decoyIP = [ip for ip in [p[IP].src, p[IP].dst] if ip in decoys]
        # Tests if each sniffed packet is in the decoy list.
        if len(decoyIP) > 0:
            ports = None
            if p.haslayer(TCP):
                ports = [p[TCP].sport,p[TCP].dport]
            elif p.haslayer(UDP):
                ports = [p[UDP].sport,p[UDP].dport]
            # After checking that a decoy IP has been contacted, these conditions see if the pull out the ports used,
            decoyPort = [port for port in ports if port in decoys[decoyIP[0]]]
            # and tests the ports against the decoy ports to fully qualify if the decoys were contacted.
            # We would want to test this because decoys can share IP adresses with production systems.
            if len(decoyPort) > 0:
                wrpcap("out.pcap",p,append=True)
                # If a true decoy was used, the packet is written to a .pcap file.

sniff(prn=analyzePackets)
