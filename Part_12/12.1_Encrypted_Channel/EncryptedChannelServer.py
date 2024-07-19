# This script sets up the AES server/recipient, connected to mirrored "client."

import socket
from Crypto.Cipher import AES

host = "127.0.0.1"
port = 1337
key = b"Sixteen byte key"

def decrypt(data,key,iv):
    cipher = AES.new(key,AES.MODE_CBC,iv)
    return cipher.decrypt(data)

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
# See client-side script for explanation up to this point.
    s.bind((host,port))
    s.listen()
    # "Listens" on the port specified in the bind() function, rather than "connecting" on the client side.
    conn,addr = s.accept()
    with conn:
        while True:
        # An Infinite loop with the client is established if the "accepted" connection is established.
            iv = conn.recv(16)
            length = conn.recv(1)   
            # It assumes only a single byte message - in this case - after the IV.
            data = conn.recv(1024)
            # the recv() function sets a max data limit. In this case it has a lot of padding, but will not result in an error in such a case.
            if not data:
                break
            print("Received: %s"%decrypt(data,key,iv).decode("utf-8")[:ord(length)])
            # Does the actual decrypting, and prints the results without "padding."
