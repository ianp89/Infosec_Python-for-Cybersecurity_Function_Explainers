# This script compares bidirectional flow data to get a broad idea about client:server relationships and server functions.
# If you know your network, and the flows do not make sense, this script is also useful to compare with expected values.

from scapy.all import *

flowData = {}
def analyzeFlow(p):
    if p.haslayer(IP):
        length = p[IP].len
        # Will miss non-IP packets, but easily modifiable.
        # Also TCP outweights UDP in length by far, but the two will balance each other when analyzing bidirectional flow.
    else:
        return
    key = None
    data = None
    if p[IP].src < p[IP].dst:
        key = ','.join([p[IP].src,p[IP].dst])
        data = [length,0]
    else:
        key = ','.join([p[IP].dst,p[IP].src])
        data = [0,length]
    # This if: else block guarantees that the src/dst are always grouped with one side of the flow because one IP will always be smaller.
    # Sorted in this way, a dictionary is created with the source of the packet (src or dst) as key, and packet as value.
    if key in flowData:
        f = flowData[key]
        flowData[key] = [f[0]+data[0],f[1]+data[1]]
    else:
        flowData[key] = data
    # This if: else block ensures keys are unique, and adds data as a value when a key is already in use.

packets = rdpcap("http.cap")
for p in packets:
    analyzeFlow(p)
# For sake of example, a pcap file is being used instead of a live capture, which would also work.

for f in flowData:
    [src,dst] = f.split(",")
    d = flowData[f]
    print("%d bytes %s->%s\t%d bytes %s->%s" % (d[0],src,dst,d[1],dst,src))
    # This prints the amount of bytes flowing in each direction by comparing the dictionary values attaches to src/dst keys.
