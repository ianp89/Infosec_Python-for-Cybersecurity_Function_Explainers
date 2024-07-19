# This script catches a threat actor killing a process, and records the PID of the process that killed it.
# It then goes ahead and actually kills the process so the actor does not know they were caught.

import signal,sys
from time import sleep

def terminated(signum,frame):
    pass
# This function does nothing, but catches a signal. Can fill in with other code to actual respond.
# Nevertheless, the function is called below when SIGTERM and SIGINT are executed on the system.

signal.signal(signal.SIGTERM,terminated)
signal.signal(signal.SIGINT,terminated)
# SIGTERM and SIGINT are "catchable" signal processes, meaning if someone were to execute a signal on a system (like Ctrl+C AKA terminate),
# the system can perform other tasks before/if the signal's function is actually executed.
while True:
    siginfo = signal.sigwaitinfo({signal.SIGINT,signal.SIGTERM})
    # This process simply waits to catch a SIGINT or SIGTERM.
    with open("terminated.txt","w") as f:
        f.write("Process terminated by %d\n" % siginfo.si_pid)
        # If caught, the process id that terminated the process is recorded in a .txt document,
    sys.exit(0)
    # but the process actually gets shut down, making the malicious actor think he got away with it.
