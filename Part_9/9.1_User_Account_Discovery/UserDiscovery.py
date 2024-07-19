# This script gathers user accounts with Admin privileges, enumerates other accounts and their password policies in Windows.

import os,wmi

w = wmi.WMI()
# "w" becomes the medium through which Python interacts with WMI.

admins = None
for group in w.Win32_Group():
    if group.Name == "Administrators":
    # First get a list of groups, and look for Administrator level.
        admins = [a.Name for a in group.associators(wmi_result_class="Win32_UserAccount")]
        # This finds available user accounts with Admin privileges!

for user in w.Win32_UserAccount():
    print("Username: %s" % user.Name)
    print("Administrator: %s" % (user.Name in admins))
    print("Disabled: %s" % user.Disabled)
    print("Local: %s" % user.LocalAccount)
    print("Password Changeable: %s"%user.PasswordChangeable)
    print("Password Expires: %s" % user.PasswordExpires)
    print("Password Required: %s" % user.PasswordRequired)
    print("\n")
# This for loop enumerates usernames, if the accounts are enabled or local, and gets password policy info for each account.

print("Password Policy:")
print(os.system("net accounts"))
# Prints Windows Password Policy (a whole view rather than above where password info is attached to usernames.).
