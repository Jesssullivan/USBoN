"""
A WIP @ the D&M Makerspace
written by Jess @ github/jesssullivan

"""

from configuration import *

# track destination addresses:
ip_conf_dict = {}

# initialize Flask app:
app = Flask(__name__, template_folder=rel_templates, static_url_path=inpath)

# app modification for pug/jade, Jinja2 is more common
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


# regenerate a persistent zip archive only if anyone requests from /downloads:
def check_archive():
    if not os.path.isfile('client-sh.zip'):
        archive = zipfile.ZipFile(os.path.join(downloads, 'client-sh.zip'), "w", zipfile.ZIP_DEFLATED)
        for f in os.listdir(downloads):
            archive.write(os.path.join(downloads, f), arcname=f)
        archive.close()


@app.route('/conf', methods=['GET', 'POST'])
def conf():
    if not ip_conf_dict.__contains__(request.remote_addr):
        ip_conf_dict[request.remote_addr] = {}
        attributes = requests.request(method='get',
                                      url='http://' + request.remote_addr +
                                          ':' + str(thing_port) + '/attributes').json()
        ip_conf_dict[request.remote_addr] = attributes

    return render_template('server_home.jade',
                           server_addr=my_addr,
                           your_addr=str(request.remote_addr),
                           available='Whoo! Added ' + ip_conf_dict[request.remote_addr]['name'])


@app.route('/', methods=['GET', 'POST'])
def home():
    available_names = []

    for addr in ip_conf_dict:
        try:
            available_names.append(ip_conf_dict[addr]['name'])
        except:
            v('err while no addresses found in ip_conf_dict, continuing...')

    if len(available_names) < 1:
        available_names.append('No visitors yet....')

    return render_template('server_home.jade',
                           server_addr=my_addr,
                           your_addr=str(request.remote_addr),
                           available=available_names)


@app.route('/download_sh', methods=['GET', 'POST'])
def download():
    check_archive()
    response = send_from_directory(downloads, filename='client-sh.zip')
    response.headers["Content-Disposition"] = str('attachment; filename=' + 'client-sh.zip')
    return response


if __name__ == '__main__':
    app.run(port=server_port)
