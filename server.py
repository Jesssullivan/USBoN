import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from optparse import OptionParser
import subprocess
from time import sleep
from requests import get

addr = get('https://api.ipify.org').text
port = 8888
bus_id = '1-1'  # default value, can be overwritten in post req


def shell(cmd):
    proc = subprocess.Popen(cmd, shell=True,
                            executable='/bin/bash',
                            encoding='utf8')
    return proc.pid


def isworking(proc):

    # using Linux PID status values if needed-
    # in this case, finished command will use except value.

    cmd = str('ps -q ' + str(proc) + ' -o state --no-headers')

    check = subprocess.Popen(cmd,
                             shell=True,
                             executable='/bin/bash',
                             encoding='utf8',
                             stdout=subprocess.PIPE)
    try:
        if check.stdout.read()[0] != 'S':
            return False
        else:
            return True
    except:
        return False


def setup():  # assuming server is run as admin!

    cmd = 'modprobe vhci-hcd && sleep 1'

    set = shell(cmd)
    sleep(.5)

    cont = False

    while not cont:
        if not isworking(set):
            cont = True
        else:
            sleep(.5)


def attach(remote, bus_id):  # assuming server is run as admin!

    attach = str('usbip attach -r ' + remote + ' -b ' + bus_id)

    try:
        shell(attach)
        sleep(.5)
    except:
        print('\n attempted attach, continuing... \n')


class RequestHandler(BaseHTTPRequestHandler):

    def post(self):
        self.send_response(200)
        self.end_headers()
        request_headers = self.headers

        # parse request - json:
        content_length = request_headers.get('Content-Length')
        length = int(content_length) if content_length else 0
        remote = json.loads(self.rfile.read(length))

        print(str('\n received remote address : ' + remote['ip'] + '\n'))

        # check  bus_id value in from request:
        if len(remote['bus']) > 1:
            bus_id = remote['bus']
            print(str('using bus_id ' + bus_id + ' - provided by remote \n' ))
        else:
            bus_id = '1-1'  # default.

        # try attach:
        try:
            attach(remote['ip'], bus_id)
        except:
            print(str('error while attaching bus_id ' + bus_id +
                      ' from remote ' + remote['ip'] + ' ... \n ' +
                      'continuing ... \n'))


def serve(addr, port):
    server = HTTPServer((addr, port), RequestHandler)
    server.serve_forever()
    parser = OptionParser()
    (options, args) = parser.parse_args()


def main(addr, port):
    print('setting up vhci-hcd \n ...')
    sleep(.2)
    print(str("\n This Server's Address is: \n\n " + 
               addr + '\n\n'))
    setup()
    print(' ... ')
    sleep(1)
    print(str('\n starting http server at: \n' +
              addr + '\n' +
              'port =' + str(port) + '\n'))
    
    serve(addr, port)


if __name__ == '__main__':
    main(addr, port)
