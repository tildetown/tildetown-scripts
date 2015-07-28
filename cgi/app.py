import json
import os
import time
from sys import argv
from tempfile import mkdtemp, mkstemp
from flask import Flask, render_template, request, redirect

SITE_NAME = 'tilde.town'

app = Flask('~cgi')

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
    return "RANDOM"

@app.route('/guestbook', methods=['GET'])
def get_guestbook():
    data_dir = app.config['DATA_DIR']
    # TODO sort by timestamp
    posts = map(lambda p: json.loads(slurp(os.path.join(data_dir, p))), os.listdir(data_dir))

    context= {
        "site_name": SITE_NAME,
        "posts": posts,
    }
    return render_template('guestbook.html', **context)

@app.route('/guestbook', methods=['POST'])
def post_guestbook():
    save_post(request.form['name'], request.form['message'])
    return redirect("/guestbook")

@app.route('/helpdesk', methods=['GET'])
def helpdesk():
    return "HELPDESK"

if __name__ == '__main__':
    if len(argv) == 2:
        data_dir = argv[1]

    else:
        data_dir = mkdtemp()

    app.config['DEBUG'] = True
    app.config['DATA_DIR'] = data_dir

    app.run()
