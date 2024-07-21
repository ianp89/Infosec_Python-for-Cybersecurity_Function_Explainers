# This script creates a baseline by recording each process running on a system (do this part when sure system is clean!),
# to see if it has a connection attached to it. And then checks against a threshold if a point-in-time connection is likely to be malicious
# using the baseline proportion of time that the process had a connection.

import psutil
# PYthon's psutil library is OS-agnostic, giving access to information about processes running on a system.

conn_counts = {}
totalConns = 0

def buildBaseline():
    for p in psutil.pids():
        proc = psutil.Process(p)
        name = proc.name()
        hasConns = int(len(proc.connections()) > 0)
        # So far this function has run through each running process on the system, named it, and tested it for connectivity.
        # hasConns uses int() to convert a boolean value to a 1 or 0...cool!
        if name in conn_counts:
            (connected,total) = conn_counts[name]
            conn_counts[name] = (connected+hasConns,total+1)
        else:
            conn_counts[name] = (hasConns,1)
        # The if: else block populates the conn_counts dictionary, first checking if the process is already a key,
        # and tallying how many instances of the process are present in total, and how many of those have connectivity.

threshold = .5
# This threshold is here as an example, but really should be tweaked (per process) based on the baseline over time.
def checkConnections():
    for p in psutil.pids():
        proc = psutil.Process(p)
        name = proc.name()
        hasConns = len(proc.connections()) > 0
        # Up to this point is the same, but rather than convert the boolean for tallying, it wants to know if the process at a point in time has a connection.
        if hasConns:
        # This if block wants to check if having a connection is suspicious.
            if name in conn_counts:
                (connected,total) = conn_counts[name]
                prob = connected/total
                # If the process is baselined, this if block calculates the probability of it rightfully having connectivity.
                if prob < threshold:
                    print("Process %s has network connection at %f probability" % (name,prob))
            else:
                print("New process %s has network connection" % name)
        else:
        # This else block wants to check if not having a connection is suspicious (for instance a browser process without a connection.)
            if name in conn_counts:
                (connected,total) = conn_counts[name]
                prob = 1-(connected/total)
                if prob < threshold:
                    print("Process %s doesn't have network connection at %f probability" % (name, prob))
            
buildBaseline()
checkConnections()
