"""
A WIP @ the D&M Makerspace
written by Jess @ github/jesssullivan
"""
from flask import Flask, render_template, send_from_directory, request, jsonify
import requests
import os
import subprocess
from requests import get
import time
import zipfile

# flask ports:
thing_port = 4999
server_port = 5000

# local address:
my_addr = get('https://api.ipify.org').text

# run as dry run?
dry = True

# verbose logging?
verbose = True

# usb port:
usb_port = '1-1.2'

# define Flask app:
app = Flask(__name__, template_folder='templates')

# modification for pug/jade, Jinja2 is more common
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

# paths:
rootpath = os.path.abspath(os.curdir)
inpath = os.path.join(rootpath, 'uploads')
outpath = os.path.join(rootpath, 'downloads')
rel_templates = os.path.relpath('templates')
templates = os.path.relpath('templates')
downloads = os.path.relpath('downloads')


def v(words):
    if verbose:
        time.sleep(.15)
        print(str(words))
        time.sleep(.15)


def shell(cmd):
    try:
        proc = subprocess.Popen(cmd,
                                shell=True,
                                executable='/bin/bash')
        return proc.pid
    except:
        print('moving on...')


def proc_wait(proc):  # bool
    init_time = time.time()
    while proc:
        time.sleep(.25)
        print(' ... ')
        if time.time() - init_time >= 10:
            print('err timeout, exiting ... ')
            quit()


def try_request(val):
    try:
        print('\n received ' + request.form.get(val) + ' ! \n ')
        return True
    except TypeError:
        return False
