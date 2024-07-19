# This script catches threat actors meddling with decoy files (which would be files set up to look enticing to catch just such people).

import pathlib

def getTimestamps(filename):
    fname = pathlib.Path(filename)
    stats = fname.stat()
    if not fname.exists(): 
        return []
        # This would mean the file got deleted...also a clear sign of tampering.
    return(stats.st_ctime,stats.st_mtime,stats.st_atime)
    # The format of decoys.txt is such that it records legitimate creation (c), modification (m), and access (a) times.
    

def checkTimestamps(filename,create,modify,access):
    stats = getTimestamps(filename)
    if len(stats) == 0:
        return False 
    (ctime,mtime,atime) = stats
    if float(create) != float(ctime):
        return False    
    elif float(modify) != float(mtime):
        return False    
    elif float(access) != float(atime):
        return False    
    return True
    # Tests the decoy files against the legitimate values. If any changes have been made, the checkDecoyFiles function sends an alert.

def checkDecoyFiles():
    with open("decoys.txt","r") as f:
    # decoys.txt contains timestamps for two decoy files.
        for line in f:
            vals = line.rstrip().split(",")
            if not checkTimestamps(vals[0],vals[1],vals[2],vals[3]):
            # Because the file contains the legitimate timestamps for the decoys, 
            # any tampering will come across as a change in one of the time values in the monitoring doc, decoys.txt.
                print("%s has been tampered with." % vals[0]

checkDecoyFiles()
