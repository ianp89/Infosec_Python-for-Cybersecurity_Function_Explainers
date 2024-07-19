# This script searches a local system for email storage and reveals full emails if stored locally.

from libratom.lib.pff import PffArchive
# The PffArchive function knows how to parse stored .pst files (Outlook email format).
# Python's libratom library in general provides wide-ranging email analysis functionality.

filename = "C:\\Users\\hepos\\Documents\\Outlook Files\\howard@howardposton.com.pst"
# This would be the location of locally stored emails using Outlook client for specified local user and email address.  
archive = PffArchive(filename)

for folder in archive.folders():
    if folder.get_number_of_sub_messages() != 0:
        for message in folder.sub_messages:
            print("Sender: %s" % message.get_sender_name())
            print("Subject: %s" % message.get_subject())
            print("Message: %s" % message.get_plain_text_body())
# Iterates through Outlook storage location specified above, tests if it has messages stored, and then reveals any emails that are there.
# Could use Regex afterwards to search for information there, for instance.
