# This file enumerates publicly facing systems of a specified domain name by providing their name, type, and IP addresses (where applicable).
# It does this by taking a partial domain name (PQDN) and iteratively testing common FQDNs associated with the root domain.
# It makes sense to start at the bottom and work your way up in this case (as the instructor of the course and author of the script did).

import dns
import dns.resolver
import socket

def ReverseDNS(ip):
    try:
        result = socket.gethostbyaddr(ip)
    except:
        return []
    return [result[0]]+result[1]
    # The socket function used above stores the main subdomain name in its first result space ('result[0]'),
    # and any alternatives are stored in "result[1]". So by running a reverse DNS query, no alternative names are missed.

def DNSRequest(domain):
    try:
        result = dns.resolver.resolve(domain, 'A')
        # The line above uses Python's dns library to return the "A record" from the provided domain's DNS system.
        # "A records" are the primary DNS type, mapping IPv4 addresses to domain names. 
        if result:
            print(domain)
            for answer in result:
                print(answer)
                print("Domain Names: %s" % ReverseDNS(answer.to_text()))
                # This block takes subdomains that successfully return an IP address above, 
                # and returns the hostname of the given A-record in case it has multiple functions not named by the subdomain name alone.
    except (dns.resolver.NXDOMAIN, dns.exception.Timeout):
        return []

def SubdomainSearch(domain, dictionary,nums):
    for word in dictionary:
        subdomain = word+"."+domain
        DNSRequest(subdomain)
        # With "dictionary" being the list of common subdomains taken from the "subdomains.txt" file below,
        # this function iterates through each subdomain and creates the full domain name (e.g. www.google.com), 
        # and then retrieves its IP address using the "DNSRequest" function, explained above.
        if nums:
            for i in range(0,10):
                s = word+str(i)+"."+domain
                DNSRequest(s)
                # Similarly, it is common practice for each subdomains to be spread across multiple hosts, often in the background.
                # For instance "wwww1.google.com," "www2..." and so on.
                # So this part of the function iterates through 10 sub-subdomains. It could do more, but for time's sake stops there.
                # Note: if want to skip this step set third variable in function call to "False" (see below).

domain = "google.com"
d = "subdomains.txt"
dictionary = []
with open(d,"r") as f:
    dictionary = f.read().splitlines()
    # The previous four lines use built-in Python functionality to create a list of Google subdomains
    # by opening a file within the current directory ('subdomain.txt') that contains common subdomains for any given IT infrastructure.
    # For instance, 'www' is the most publicly consumed subdomain type, serving up web content. 
    # This function tests the most common, and "subdomains.txt" is extensible to expand the search.
SubdomainSearch(domain,dictionary,True)
# Example here calls "Subdomain Search" on Google to enumerate publicly-facing, but otherwise publicly-unknown systems.
