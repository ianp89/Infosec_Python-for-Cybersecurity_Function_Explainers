# This script sets up an AES client to encrypt messages sent on a specific port.

import socket, os
from Crypto.Cipher import AES

host = "127.0.0.1"
port = 1337
key = b"Sixteen byte key"
# This theoretical encrypted channel functions solely on port 1337 of the local host, 
# but this information would be modified for sender and recipient.
# AES works with a pre-shared key, given here as "key."

def encrypt(data,key,iv):
    data += " "*(16 - len(data) % 16)
    # AES only works for data in 16 byte blocks, so this line finds how many spaces necessary to complete 16 bytes (= 'padding').
    cipher = AES.new(key,AES.MODE_CBC,iv)
    # CBC is a "mode of operation," needs to be identical on both sides of the connection;
    #basically establishes how the encryption method deals with data longer than its maximum encryptable datablock size.
    return cipher.encrypt(bytes(data,"utf-8"))

message = "Hello"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host,port))
    # Python's socket library is used here to send data through the specificied port (here = 1337).
    iv = os.urandom(16)
    s.send(iv)
    # Appropriately sized Initialization Vector (iv) is used to initiate AES cipher in CBC mode. IV's are used to further obscure data by 
    # adding an element of randomness to the beginning of a data stream.
    s.send(bytes([len(message)]))
    # Informs the server how long the message is (could be implemented in padding statement).
    encrypted = encrypt(message,key,iv)
    print("Sending %s" % encrypted.hex())
    s.sendall(encrypted)
    # Encrypted message sent.
