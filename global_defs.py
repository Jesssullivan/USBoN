from flask import Flask, render_template, send_from_directory, request, redirect, url_for
import requests
from requests import get
import os
import subprocess
import threading
from requests import get, post
import time
import zipfile
import json

# paths:
rootpath = os.path.abspath(os.curdir)
inpath = os.path.join(rootpath, 'uploads')
outpath = os.path.join(rootpath, 'downloads')
rel_templates = os.path.relpath('templates')
templates = os.path.relpath('templates')
downloads = os.path.relpath('downloads')

# usb port:
usb_port = '1-1.2'


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