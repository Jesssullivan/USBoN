# by Jess Sullivan  @ The D&M Makerspace

from global_defs import *

# server ip:
self_addr = str(get('https://api.ipify.org').text)

# track usbip destination addresses:
ip_dict = {}

# define Flask app:
app = Flask(__name__, template_folder=rel_templates, static_url_path=inpath)

# app modification for pug/jade, Jinja2 is more common
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


def check_archive():
    if not os.path.isfile('client-sh.zip'):
        archive = zipfile.ZipFile(os.path.join(downloads, 'client-sh.zip'), "w", zipfile.ZIP_DEFLATED)
        for f in os.listdir(downloads):
            archive.write(os.path.join(downloads, f), arcname=f)
        archive.close()


@app.route('/')
def home():

    print(request.remote_addr)  # log visitor

    def visitors():
        if len(ip_dict.items()) < 1:
            return '...no things online yet  :('
        else:
            avail = ''
            for thing in ip_dict.keys():
                avail += str(thing['name']) + ' is available! \n'
            return avail

    return render_template('home.jade',
                           server_addr=self_addr,
                           your_addr=str(request.remote_addr),
                           available=visitors())


@app.route('/conf', methods=['GET', 'POST'])
def conf():
    ip_dict[request.remote_addr] = request.remote_addr
    attr_read= requests.get('http://' + request.remote_addr + '/attributes').json
    attributes = json.load(attr_read)
    # todo - ....


@app.route('/available', methods=['GET', 'POST'])
def available():
    ip_dict[request.remote_addr] = request.remote_addr
    print(request.is_json)
    content = request.get_json()
    print(content)
    return 'JSON posted'


@app.route('/attachremote', methods=['GET', 'POST'])
def addremote():
    try:
        shell('usbip attach -r  ' + str(request.remote_addr) + ' -b 1-1.2')
    except:
        print('continuing...')
    return render_template('home.jade',
                           server_addr=self_addr,
                           your_addr=str(request.remote_addr),
                           is_enabled=str(ip_dict.__contains__(request.remote_addr)))


@app.route('/download_sh', methods=['GET', 'POST'])
def download():
    check_archive()
    response = send_from_directory(downloads, filename='client-sh.zip')
    response.headers["Content-Disposition"] = str('attachment; filename=' + 'client-sh.zip')
    return response


if __name__ == '__main__':
    app.run()


