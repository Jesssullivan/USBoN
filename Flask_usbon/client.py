import requests
import socket
import threading
import subprocess
from time import sleep
from sys import argv

# server: destination to send client's address to
host_addr = '10.206.1.157'  # default addr- updates as argument
port = 8888

# client:
bus_id = '1-1'  # default- can send alternative bus_id to server w/ json
hostname = socket.gethostname()
my_addr = socket.gethostbyname(hostname)


def argtype():
    try:
        if len(argv) > 1:
            use = True
        elif len(argv) == 1:
            use = False
        else:
            print('command takes 0 or 1 args')
            raise SystemExit
    except:
        print('arg error... \n command takes 0 or 1 args')
        raise SystemExit
    return use


def shell(cmd):
    proc = subprocess.Popen(cmd, shell=True,
                            executable='/bin/bash',
                            encoding='utf8')
    return proc.pid


def isworking(proc):

    cmd = str('ps -q ' + str(proc) + ' -o state --no-headers')

    check = subprocess.Popen(cmd,
                             shell=True,
                             executable='/bin/bash',
                             encoding='utf8',
                             stdout=subprocess.PIPE)

    if check.stdout.read()[0] != 'S':
        return False
    else:
        return True


def setup():  # assuming all as admin

    cmd = 'modprobe usbip_host && sleep 1'

    set = shell(cmd)
    sleep(.5)

    cont = False

    while not cont:
        if not isworking(set):
            cont = True
        else:
            sleep(.5)


def bind(bus_id):

    unbind = str(' usbip unbind -b ' + bus_id + ' && sleep 1 && ')
    bind = str(' usbip bind -b ' + bus_id)

    try:
        shell(unbind)
        sleep(.5)
    except:
        print('\n attempted unbind, continuing... \n')

    shell(bind)


def start_daemon():
    daemon = threading.Thread(target=shell('nohup usbipd &'), daemon=True)
    daemon.start()


def main(host_addr, my_addr, port, bus_id):
    # send ip address to server:
    received = False
    while not received:
        # POST request sent as JSON:
        res = requests.post(str('http://' + host_addr + ':' + str(port) + '/'),
                            json={"ip": my_addr,
                                  "bus": bus_id})

        if res.status_code == 200:
            print(str('Successfully sent IP to http server! \nMy IP is: ' + my_addr))
            received = True
        else:
            sleep(1)

    if received:
        setup()
        sleep(.1)
        start_daemon()
        sleep(.1)
        bind(bus_id)


if __name__ == '__main__':
    
    if argtype:
        addr = argv[1]
    
    main(host_addr, my_addr, port, bus_id)
