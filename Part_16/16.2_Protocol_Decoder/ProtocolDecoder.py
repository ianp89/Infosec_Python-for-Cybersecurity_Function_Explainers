# This script depends on scripts from Module 12.2.

from scapy.all import *
from scapy.layers.http import *
from base64 import b64decode

b64regex = b"[A-Za-z0-9+/=]+"
def extractData(data):    
    data = data.rstrip()
    matches = re.findall(b64regex,data)
    # Cleans data and limits search within the data to match possibilities that are encoded in base64.
    for match in matches:
        if len(match) == 0:
            continue
        try:
            if not len(match) % 4 == 0:
                padnum = (4-len(match)%4)%4
                match += b"=" * padnum
                # base64 requires data in 4-byte chunks; so if exfiltrator stripped "padding" (always '=' in base64)
                # to better hide their activity, this appends padding in order for base64 decoding to be possible (next line).                 
            decoded = b64decode(match).decode("utf-8")
            if len(decoded) > 5 and decoded.isprintable():
                # This is arbitrary...only returns data if greater than 5 bytes.
                print("Decoded: %s"%decoded)
        except:
            continue

def extractHTTP(p):
    fields = None
    if p.haslayer(HTTPRequest):
        fields = p[HTTPRequest].fields
    else:
        fields = p[HTTPResponse].fields
    for f in fields:
        data = fields[f]
    # Processes HTTP data from both requests and response so Python can do further processing more easily.
        if isinstance(data,str):
            extractData(data)
        elif isinstance(data,dict):
            for d in data:
                extractData(data[d])
        elif isinstance(data,list) or isinstance(data,tuple):
            for d in data:
                extractData(d)
        # Checks which data type the data contains in order to send it in appropriate form to extractData() (above).

def extractRaw(p):
    extractData(p[Raw].load)
    # Processes the "raw" data to be sent to extractData() (above). 

def analyzePackets(p):
    if p.haslayer(HTTPRequest) or p.haslayer(HTTPResponse):
        p.show()
        extractHTTP(p)
    elif p.haslayer(Raw):
        extractRaw(p)
    # After checking for HTTP or raw data in packet (two common exfil avenues...can extend for greater use of script),
    # this function pushes the packet data to one of the extract* functions (above).

sniff(prn=analyzePackets)
