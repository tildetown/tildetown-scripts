from functools import lru_cache
import json
import os
import random
import time
from sys import argv
from tempfile import mkdtemp, mkstemp

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

@lru_cache(maxsize=32)
def cfg(k):
    conf = ConfigFactory.parse_file('cfg.conf')
    return conf[k]

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
    filename_to_json = lambda p: json.loads(slurp(os.path.join(data_dir, p)))
    posts = map(filename_to_json, os.listdir(data_dir))
    sorted_posts = sorted(posts, key=lambda p: p['timestamp'], reverse=True)

    context = {
        "posts": sorted_posts,
    }
    context.update(site_context())
    return render_template('guestbook.html', **context)

@app.route('/guestbook', methods=['POST'])
def post_guestbook():
    message = request.form['message'][0:400]
    name = request.form['name'][0:140]
    captcha = request.form['hmm']
    if captcha == "scrop":
        save_post(name, message)
    return redirect("/guestbook")

@app.route('/helpdesk', methods=['GET'])
def get_helpdesk():
    status = request.args.get('status', 'unsubmitted')
    desc = request.args.get('desc', '')
    context = {
        'status': status,
        'desc': desc,
    }
    context.update(site_context())
    return render_template('helpdesk.html', **context)

def send_email(data):
    name = data.get('name', 'anonymous')
    email = data['email']
    request_type = data['type']
    desc = request.form['desc']
    response = requests.post(
        cfg('mailgun_url'),
        auth=("api", cfg('mailgun_key')),
        data={"from": "root@tilde.town",
              "to": cfg('trello'),
              "subject": "{} from {} <{}>".format(request_type, name, email),
              "text": desc})

    return response.status_code == 200

@app.route('/helpdesk', methods=['POST'])
def post_helpdesk():
    desc = request.form['desc']
    captcha = request.form['hmm']

    if captcha == 'scrop':
        status = "success" if send_email(request.form) else "fail"
    else:
        status = "fail"

    # should we bother restoring other fields beside desc?
    return redirect('/helpdesk?status={}&desc={}'.format(status, desc))

if __name__ == '__main__':
    if len(argv) == 2:
        data_dir = argv[1]
    else:
        data_dir = mkdtemp()

    app.config['DEBUG'] = True
    app.config['DATA_DIR'] = data_dir

    print("Running with data_dir=", app.config['DATA_DIR'])

    app.run()
