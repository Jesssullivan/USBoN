
from global_defs import *

# define Flask app:
app = Flask(__name__, template_folder='templates')

# modification for pug/jade, Jinja2 is more common
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

# JobServer address:
job_srv_addr = 'http://127.0.0.1:5000'  # placeholder

# thing attributes:
attributes = {}


def start_set_usb(addr):
    if os.path.isfile('.usbon.confirm'):
        print('attempting to starting usbipd.... \n')
        proc_wait(shell('usbipd & >> usbipd.log'))
        time.sleep(.5)
        print('attempting initial unbind.... \n')
        proc_wait(shell('usbip unbind -b ' + usb_port))
        time.sleep(.5)
        print('attempting bind on usb port' + usb_port + ' : \n')
        proc_wait(shell('usbip bind -b ' + usb_port))
        shell('wget ' + addr + '/addremote')


def isworking(proc):
    cmd = str('ps -q ' + str(proc) + ' -o state --no-headers')
    check = subprocess.Popen(cmd,
                             shell=True,
                             executable='/bin/bash',
                             stdout=subprocess.PIPE)

    if check.stdout.read()[0] != 'S':
        return False
    else:
        return True


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('landing.jade', my_addr=get('https://api.ipify.org').text)


@app.route('/conf', methods=['GET', 'POST'])
def conf():

    if try_request('name'):
        attributes['name'] = request.form.get('name')
    else:
        attributes['name'] = request.remote_addr

    if not try_request('jobserver'):
        job_srv_addr = 'http://127.0.0.1:5000'
    else:
        job_srv_addr = request.form.get('jobserver')
        shell('echo ' + str(job_srv_addr) + ' >> .usbon.confirm')

    if not try_request('usbon'):
        attributes['serial'] = False
    else:
        attributes['serial'] = True
        if try_request('amd'):
            attributes['platform'] = 'x86'
            shell('sudo chmod u+x usbip_install_amd-64.sh')
            time.sleep(.5)
            install_pid = shell('sudo ./usbip_install_amd-64.sh')
        else:
            attributes['platform'] = 'arm'
            shell('sudo chmod u+x usbip_install_arm.sh')
            time.sleep(.5)
            install_pid = shell('sudo ./usbip_install_arm.sh')

            while not isworking(install_pid):
                shell('touch .usbon.confirm')

    return render_template('landing.jade', my_addr=get('https://api.ipify.org').text)


if __name__ == '__main__':
    if not os.path.isfile('.usbon.confirm'):
        app.run()
    else:
        job_addr = open('.usbon.confirm').read()
        start_set_usb(job_addr)