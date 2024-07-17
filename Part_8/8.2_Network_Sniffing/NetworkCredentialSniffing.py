# This script works with PCAP data to extract username/password combos from 3 insecure protocols.

from scapy.all import *
# Python's scapy library is a packet capture and manipulation tool discussed way back in Part 2 of this course.
from base64 import b64decode
# Python's base64 is dedicated to functions working with base64 encoding
import re
# Python's Regex library.

def ExtractFTP(packet):
    payload = packet[Raw].load.decode("utf-8").rstrip()
    if payload[:4] == 'USER':
        print("%s FTP Username: %s" % (packet[IP].dst,payload[5:]))
    elif payload[:4] == 'PASS':
        print("%s FTP Password: %s" % (packet[IP].dst,payload[5:]))
# The function decodes the raw data, tests if it begins with username/password prompts, and prints the value input to the prompts if so.

emailregex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
# one example of a Regex statement that would match a standard email format of letters/numbers, possible special characters @ so-and-so.
unmatched = []
def ExtractSMTP(packet):
    payload = packet[Raw].load
    try:
        decoded = b64decode(payload)
        decoded = decoded.decode("utf-8")
        connData = [packet[IP].src,packet[TCP].sport]
        # The line above tracks client IP:Port in case there are multiple SMTP streams in the PCAP.
    # Because most of the data in a stream is not base64 encoded (only auth payloads are), most decoding operations will throw an error,
    # hence the necessity of the try block.
        if re.search(emailregex,decoded):
        # Because only logon info in base64 encoded and the string matches an email format, it is safe to assume a username has been found.
            print("%s SMTP Username: %s" % (packet[IP].dst,decoded))
            unmatched.append([packet[IP].src,packet[TCP].sport])
            # Because the username was found, safe to assume waiting for password, so add it to a list of unmatched usernames
            # that will continue to listen using the captured IP:Port information.
        elif connData in unmatched:
                print("%s SMTP Password: %s" % (packet[IP].dst,decoded))
                unmatched.remove(connData)
                # After catching the password that was anticipated, the sniffing can end, because username and password were captured.
    except:
        return

awaitingLogin = []
awaitingPassword = []
def ExtractTelnet(packet):
    try:
        payload = packet[Raw].load.decode("utf-8").rstrip()
        # Again, only usernames and passwords are decodeable using utf-8, so the rest of the data can be ignored for present purposes.
    except:
        return
    connData = [packet[IP].src,packet[TCP].sport] 
    # Assuming server is the source, start storing sessions information here. The server "challenges" the client 
    # with username and password prompts in the case of FTP.
    if payload[:5] == "login":
        awaitingLogin.append(connData)
        return
    elif payload[:8] == "Password":
        awaitingPassword.append(connData)
        return
    connData = [packet[IP].dst,packet[TCP].dport] 
    # Assuming client is the source now because we are waiting to sniff a response to the challenge prompt.
    if connData in awaitingLogin:
        print("%s Telnet Username: %s" % (packet[IP].dst,payload))
        awaitingLogin.remove(connData)
    elif connData in awaitingPassword:
        print("%s Telnet Password: %s" % (packet[IP].dst,payload))
        awaitingPassword.remove(connData)
    # This if, elif block captures the information responding to the server and removes the session information from the list.

packets = rdpcap("merged.pcap")
# Gives a list of packets "read from (named) pcap" file

for packet in packets:
    if packet.haslayer(TCP) and packet.haslayer(Raw):
        if packet[TCP].dport == 21:
            ExtractFTP(packet)
        elif packet[TCP].dport == 25:
            ExtractSMTP(packet)
        elif packet[TCP].sport == 23 or packet[TCP].dport == 23:
            ExtractTelnet(packet)
# This for loop iterates over all the captured packets and separates out TCP packets on specified ports with data payload in them ('Raw').
