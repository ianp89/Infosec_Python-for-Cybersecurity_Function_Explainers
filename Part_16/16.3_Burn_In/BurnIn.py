# Burn-in creates realistic looking network traffic to make a decoy look more attractive assuming attacker can monitor traffic.
# This script creates a "reasonably plausible" looking browsing session to make it look that network traffic is legitimate.

import random, requests
from time import sleep

def makeRequest(url):
    _ = requests.get(url)
    return
    # Actually calls the URL with an HTTP request. Could tweak to actually use a browser also.
    # The _ ignored the response, but responses can be used for web crawling...interesting!

def getURL():
    return sites[random.randint(0,len(sites)-1)].rstrip()
    # Returns a random URL from sites.txt.

clickthrough = .5
# This is a 50% chance.
sleeptime = 1
# Represents how long a user would spend on page if this weren't just a script. haha
def browsingSession():
    while(random.random() < clickthrough):
        url = getURL()
        makeRequest(url)
        sleep(random.randint(0,sleeptime))
        # Creates random amount of clicks where hypothetical user spends a random amount of time at each site.
        
f = open("sites.txt","r")
sites = f.readlines()
# sites.txt is an extensible list of commonly visited URLs that will be called to generate traffic.

browsingSession()
