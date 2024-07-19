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
    # AES only works for data in 16 byte blocks, so this line finds how many spaces necessary to complete 16 bytes.
    cipher = AES.new(key,AES.MODE_CBC,iv)
    # CBC is a "mode of operation," needs to be identical on both sides of the connection;
    #basically establishes how the encryption method deals with data longer than its maximum encryptable datablock size.
    return cipher.encrypt(bytes(data,"utf-8"))

message = "Hello"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host,port))
    iv = os.urandom(16)
    s.send(iv)
    s.send(bytes([len(message)]))
    encrypted = encrypt(message,key,iv)
    print("Sending %s" % encrypted.hex())
    s.sendall(encrypted)
