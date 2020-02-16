"""
A WIP @ the D&M Makerspace
written by Jess @ github/jesssullivan
"""

from configuration import *

# initialize addresses:
job_srv_addr = 'http://127.0.0.1:5000'  # placeholder
my_addr = get('https://api.ipify.org').text

# thing attributes:
attributes = {}


def start_set_usb():
    # default behavior on boot, after all is configured
    if os.path.isfile('.usbon.confirm'):
        v('found confirmation file;  attempting to starting usbipd.... \n')
        if not dry:
            proc_wait(shell('usbipd & >> usbipd.log'))
            time.sleep(.5)

        v('attempting initial unbind.... \n')
        if not dry:
          proc_wait(shell('usbip unbind -b ' + usb_port))
          time.sleep(.5)

        v('attempting bind on usb port' + usb_port + ' : \n')
        if not dry:
            proc_wait(shell('usbip bind -b ' + usb_port))
    else:
        v('could not find confirmation file, continuing...')


# check if some spawned process is still working on pid:
def isworking(proc):
    if not dry:
        cmd = str('ps -q ' + str(proc) + ' -o state --no-headers')
        check = subprocess.Popen(cmd,
                                 shell=True,
                                 executable='/bin/bash',
                                 stdout=subprocess.PIPE)
        if check.stdout.read()[0] != 'S':
            return False
        else:
            return True
    else:
        print('halting, dry run cannot spawn exec shell!')
        raise SystemExit


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('client_landing.jade', my_addr=my_addr)


@app.route('/conf', methods=['GET', 'POST'])
def conf():

    if try_request('name'):
        attributes['name'] = request.form.get('name')
    else:
        attributes['name'] = request.form.get(request.remote_addr)

    if try_request('jobserver'):
        attributes['jobserver'] = request.form.get('jobserver')
    else:
        attributes['jobserver'] = request.form.get('job_srv_addr')

    if try_request('usbon'):
        attributes['serial'] = True
    else:
        attributes['serial'] = False

    if try_request('video'):
        attributes['video'] = True
    else:
        attributes['video'] = False

    if try_request('amd'):
        attributes['platform'] = 'x86'
    else:
        attributes['platform'] = 'arm'

    if not dry:
        v('adding jobserver address to confirmation file...')
        shell('echo ' + attributes['jobserver'] + ' >> .usbon.confirm')
        time.sleep(.25)
        if attributes['amd']:
            v('preparing installation script for amd-64....')
            shell('sudo chmod u+x usbip_install_amd-64.sh')
            v('\n....installing....\n')
            install_pid = shell('sudo chmod u+x usbip_install_amd-64.sh')
        else:
            v('preparing installation script for arm....')
            shell('sudo chmod u+x usbip_install_arm.sh')
            v('\n....installing....\n')
            install_pid = shell('sudo chmod u+x usbip_install_arm.sh')
            install_pid = shell('sudo ./usbip_install_arm.sh')

        # add persistent placeholder:
        while not isworking(install_pid):
            shell('touch .usbon.confirm')

    # NOTIFY JOB SERVER:
    shell('wget ' + attributes['jobserver'] + '/conf')

    # notify user:
    return render_template('client_complete.jade', my_addr=my_addr)


# attributes are hosted here:
@app.route('/attributes', methods=['GET', 'POST'])
def serve_attributes():
    return jsonify(attributes)


if __name__ == '__main__':
    if not os.path.isfile('.usbon.confirm'):
        app.run(port=thing_port)
    else:
        start_set_usb()
