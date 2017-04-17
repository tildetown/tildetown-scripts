from functools import lru_cache
import json
import os
import random
import time
from sys import argv
from tempfile import mkdtemp, mkstemp
import logging

from pyhocon import ConfigFactory
import requests
from flask import Flask, render_template, request, redirect

from tildetown.stats import get_data

## disgusting hack for python 3.4.0
import pkgutil
orig_get_loader = pkgutil.get_loader
def get_loader(name):
    try:
        return orig_get_loader(name)
    except AttributeError:
        pass
pkgutil.get_loader = get_loader
##########

SITE_NAME = 'tilde.town'

app = Flask('~cgi')

app.config['DEBUG'] = True
# tension between this and cfg function...

conf = ConfigFactory.parse_file('cfg.conf')

logging.basicConfig(filename='/tmp/cgi.log', level=logging.DEBUG)

@lru_cache(maxsize=32)
def site_context():
    return get_data()

@app.route('/random', methods=['GET'])
def get_random():
    user = random.choice(site_context()['live_users'])
    return redirect('http://tilde.town/~{}'.format(user['username']))


if __name__ == '__main__':
    app.run()
