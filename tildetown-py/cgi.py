from functools import lru_cache
import json
import os
import random
import time
from sys import argv
from tempfile import mkdtemp, mkstemp
from flask import Flask, render_template, request, redirect
from stats import get_data

## disgusting hack for python 3.4
import pkgutil
orig_get_loader = pkgutil.get_loader
def get_loader(name):
    try:
        return orig_get_loader(name)
    except AttributeError:
        pass
pkgutil.get_loader = get_loader
###########

SITE_NAME = 'tilde.town'

app = Flask('~cgi')

@lru_cache(maxsize=32)
def site_context():
    return get_data()

def slurp(file_path):
    contents = None
    with open(file_path, 'r') as f:
        contents = f.read()
    return contents

def save_post(name, message):
    timestamp = time.time()
    data = {
        'name': name,
        'message': message,
        'timestamp': timestamp,
    }
    _, file_path = mkstemp(dir=app.config['DATA_DIR'])
    with open(file_path, 'w') as f:
        f.write(json.dumps(data))

@app.route('/random', methods=['GET'])
def get_random():
    user = random.choice(site_context()['live_users'])
    return redirect('http://tilde.town/~{}'.format(user['username']))

@app.route('/guestbook', methods=['GET'])
def get_guestbook():
    data_dir = app.config['DATA_DIR']
    # TODO sort by timestamp
    posts = map(lambda p: json.loads(slurp(os.path.join(data_dir, p))), os.listdir(data_dir))

    context = {
        "posts": posts,
    }
    context.update(site_context())
    return render_template('guestbook.html', **context)

@app.route('/guestbook', methods=['POST'])
def post_guestbook():
    message = request.form['message'][0:400]
    name = request.form['name'][0:140]
    captcha = request.form['hmm']
    if captcha == "scriz":
        save_post(name, message)
    return redirect("/guestbook")

@app.route('/helpdesk', methods=['GET'])
def helpdesk():
    return "HELPDESK UNDER CONSTRUCTION"

if __name__ == '__main__':
    if len(argv) == 2:
        data_dir = argv[1]
    else:
        data_dir = mkdtemp()

    app.config['DEBUG'] = True
    app.config['DATA_DIR'] = data_dir

    app.run()
