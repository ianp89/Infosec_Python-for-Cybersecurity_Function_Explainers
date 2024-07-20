# Requiring an Admin cmd-prompt, this script detects failed logons per account.
# Not written here, but this detection could be associated to an alerting system, or some other action.

import win32evtlog
# Python's win32evtlog interacts with Windows Event Logs (a CLI Event Viewer!).

server = "localhost"
logtype = "Security"
flags = win32evtlog.EVENTLOG_FORWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
# Reads events from oldest to newest and reads sequentially.

failures = {}

def checkEvents():
    h = win32evtlog.OpenEventLog(server,logtype)
    # Opens a Python handler to isolate Security logs on the localhost.
    while True:
        events = win32evtlog.ReadEventLog(h,flags,0)
        # This variable now holds all the desired events.
        if events:
            for event in events:
                if event.EventID == 4625:
                # Example: 4625 are failed logons.
                    if event.StringInserts[0].startswith("S-1-5-21"):
                    # The specified variable is a user ID (only an example, again).
                        account = event.StringInserts[1]
                        # The 1 is the username associated with the user ID specified in the previous line.
                        if account in failures:
                            failures[account] += 1
                        else:
                            failures[account] = 1
                        # Creates a dictionary of unique usernames and number of failed logon attempts.
        else:
            break

checkEvents()

for account in failures:
    print("%s: %s failed logins" % (account,failures[account]))
# Uses the results from the created function to list failed logon attempts and their associated account information.
