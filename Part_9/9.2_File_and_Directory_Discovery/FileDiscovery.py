# This script traverses a filesystem to search within files for PII identified by Regex statements.

import os,re
from zipfile import ZipFile
# zipfile is one of Python's libraries for working with zip files.

email_regex = '[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}'
phone_regex = '[(]*[0-9]{3}[)]*-[0-9]{3}-[0-9]{4}'
ssn_regex = '[0-9]{3}-[0-9]{2}-[0-9]{4}'
# Feel free to add more options here!
regexes = [email_regex, phone_regex, ssn_regex]

def findPII(data):
    matches = []
    for regex in regexes:
        m = re.findall(regex,data)
        matches += m
    return matches
# Shockingly self-explanatory if you're already in a system! Pretty amazing.

def printMatches(filedir,matches):
    if len(matches) > 0:
        print(filedir)
        for match in matches:
            print(match)
# Verifies matches and reveals PII and file locations.
    
def parseDocx(root,docs):
# Because .docx files are basically zip files, they have a "word" and "xml" folders.
    for doc in docs:
        matches = None
        filedir = os.path.join(root,doc)
        with ZipFile(filedir,"r") as zip:
            data = zip.read("word/document.xml")
            matches = findPII(data.decode("utf-8"))
            # Works basically the same as parseText function (below) but with the added necessity of treating it as a zip file and decoding.
        printMatches(filedir,matches)

def parseText(root,txts):
# This function look within .txt docs for PII.
    for txt in txts:
        filedir = os.path.join(root,txt)
        # Points to the full file path.
        with open(filedir,"r") as f:
            data = f.read()
        matches = findPII(data)
        # After opening the file, and "reading" it, this block applies the findPII from above to locate PII matches through Regex.
        printMatches(filedir,matches)
        # Uses the printMatches function defined above to reveal PII and file locations.

txt_ext = [".txt",".py",".csv"]

def findFiles(directory):
# Goes through entire file system (with 'walk()' function) to identify certain types of files and folders, to then apply the above functions.
    for root,dirs,files in os.walk(directory):
        parseDocx(root,[f for f in files if f.endswith(".docx") ])
        for ext in txt_ext:
            parseText(root,[f for f in files if f.endswith(ext)])

directory = os.path.join(os.getcwd(),"Documents")
# One could potentially search an entire filesystem by setting one's PWD at root.
findFiles(directory)
