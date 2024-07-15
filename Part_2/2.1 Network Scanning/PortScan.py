# This is an extensible/malleable script that provides two types of network scans.

from scapy.all import *
# scapy is Python's go-to library for packet capture and manipulation, 
# integrateable with Wireshark, and even replacing it if you're good enough!

ports = [25,80,53,443,445,8080,8443]
# The ports variable will tell the SynScan function below which ports to scan on the target system.
# The value set in this particular variable is just an example. It can be set to any/how many you want/need.

def SynScan(host):
# This function is executing a SYN scan on the target, like nmap's "-sS" option.
# A SYN scan sends a SYN packet hoping for an SYN-ACK(knowledge) packet to be returned from the target system.
# The scan does not complete the "handshake" with the final acknowledgement, thus leaving an open connection request.
# A well-designed detection system will catch this open state, but many will not; therefore this is a "quiet" scan.
    ans,unans = sr(IP(dst=host)/TCP(dport=ports,flags="S"),timeout=2,verbose=0)
    # The sr() function is built into scapy. It "sends and receives" (hence 'sr')
    # Here, a TCP packet wrapped with an IP address is created.  
    # It tests the ports specified by the 'ports' variable with SYN ('S') packets. 
    # It only listens briefly (timeout), and returns the minimum output to the variables 'ans' and 'unans' (verbose=0).
    # You can also set an 'sport' variable to a specific value before dport to make Wireshark filtering easier.
    # ans receives all SYN-ACK responses automatically from the 'sr' function.
    print("Open ports at %s:" % host)
    for (s,r,) in ans:
        if s.haslayer(TCP) and r.haslayer(TCP):
            if s[TCP].dport == r[TCP].sport:
            # Looping through the "'ans'wered" packets to ensure the sending and receiving sockets were the same,
            # The function gives you a readout of open ports (or at least the ones answering session requests) on the target system. 
                print(s[TCP].dport)

def DNSScan(host):
    ans,unans = sr(IP(dst=host)/UDP(dport=53)/DNS(rd=1,qd=DNSQR(qname="google.com")),timeout=2,verbose=0)
    # Similarly to the previous function, but this one tests only for DNS responses on DNS's default port. 
    # There is less concern of alarm bells going off in this case as (at least public) DNS servers are built to answer such requests.
    # If it answers, the print statement below will tell you it is a DNS server.
    if ans:
        print("DNS Server at %s"%host)
    
host = "8.8.8.8"
SynScan(host)
DNSScan(host)
# The example here runs both functions testing one of Google's well-known public DNS servers.
