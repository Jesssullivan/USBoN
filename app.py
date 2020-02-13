"""
by Jess Sullivan  @ The D&M Makerspace
"""
from flask import Flask, render_template, send_from_directory, request
import os
from requests import get


# paths:
rootpath = os.path.abspath(os.curdir)
inpath = os.path.join(rootpath, 'uploads')
outpath = os.path.join(rootpath, 'downloads')
templates = os.path.join(rootpath, 'templates')
rel_templates = os.path.relpath('templates')

# define Flask app:
app = Flask(__name__, template_folder=rel_templates, static_url_path=inpath)

# app modifications- using pug/jade, Jinja2 is more common
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/')
def home():
    return render_template('home.jade', server_addr=str( get('https://api.ipify.org').text), your_addr=str(request.remote_addr))


@app.route('/clientusbon', methods=['GET', 'POST'])
def clientscript():
    req = request.form.get('name')
    response = send_from_directory(os.path.relpath('downloads'), filename='usbip_depends.sh')
    response.headers["Content-Disposition"] = str('attachment; filename=' + 'usbip_depends.sh')
    return response

