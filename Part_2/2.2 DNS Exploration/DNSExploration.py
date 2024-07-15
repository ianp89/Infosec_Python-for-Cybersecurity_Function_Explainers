# This file enumerates publicly facing systems of a specified domain name by providing their name, type, and IP addresses (where applicable).
# It makes sense to start at the bottom and work your way up in this case (as the instructor of the course and author of the script did).

import dns
import dns.resolver
import socket

def ReverseDNS(ip):
    try:
        result = socket.gethostbyaddr(ip)
        return [result[0]]+result[1]
    except socket.herror:
        return None

def DNSRequest(domain):
    ips = []
    try:
        result = dns.resolver.resolve(domain)
        if result:
            print(domain)
            for answer in result:
                print(answer)
                print("Domain Names: %s" % ReverseDNS(answer.to_text()))
    except (dns.resolver.NXDOMAIN, dns.exception.Timeout):
        return []
    return ips

def SubdomainSearch(domain, dictionary,nums):
    successes = []
    for word in dictionary:
        subdomain = word+"."+domain
        DNSRequest(subdomain)
        if nums:
            for i in range(0,10):
                s = word+str(i)+"."+domain
                DNSRequest(s)

domain = "google.com"
d = "subdomains.txt"
dictionary = []
with open(d,"r") as f:
    dictionary = f.read().splitlines()
    # The previous four lines use built-in Python functionality to create a list of Google subdomains
    # by opening a file within the current directory ('subdomain.txt') that contains common subdomains for any given IT infrastructure
SubdomainSearch(domain,dictionary,True)
# Example here calls "Subdomain Search" on Google to enumerate publicly-facing, but otherwise publicly-unknown systems.
