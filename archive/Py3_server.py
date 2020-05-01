"""
# Send IP address to OctoPrint server
# WIP by Jess Sullivan
#
# As of 10/28/19, OctoPrint still relies on Python2-
# verbatim conversion from Py3:
# ``` pip install 3to2 ```
# ``` 3to2 -w Py3_server.py ``` # Py3 is preserved as .bak
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
from optparse import OptionParser
import json
import subprocess

verbose = False  # use prints to console?

addr = '127.0.0.1'  # server's address
port = 8888  # must match client


class RequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        request_headers = self.headers

        # parse request (json):
        content_length = request_headers.get('Content-Length')
        length = int(content_length) if content_length else 0
        remote = json.loads(self.rfile.read(length))

        print(remote['ip'])

        # mount satellite USB:
        satellite = str('sudo usbip attach -r ' + remote['ip'] + ' -b 1-3')
        subprocess.Popen(satellite, shell=True, executable='/bin/bash')


