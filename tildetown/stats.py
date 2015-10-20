#!/usr/local/bin/python3

# tdp.py - tilde data in tilde data protocol format.
# Copyright 2015 Michael F. Lamb <http://datagrok.org>
# License: GPLv3+

"""
Outputs JSON data conforming to "~dp (Tilde Description Protocol)" as defined
at: http://protocol.club/~datagrok/beta-wiki/tdp.html

It is a JSON structure of the form:

{
    'name':         (string) the name of the server.
    'url':          (string) the URL of the server.
    'signup_url':   (string) the URL of a page describing the process required to request an account on the server.
    'user_count':   (number) the number of users currently registered on the server.
    'want_users':   (boolean) whether the server is currently accepting new user requests.
    'admin_email':  (string) the email address of the primary server administrator.
    'description':  (string) a free-form description for the server.
    'users': [      (array) an array of users on the server.
        {
            'username': (string) the username of the user.
            'title':    (string) the HTML title of the user’s index.html page.
            'mtime':    (number) a timestamp representing the last time the user’s index.html was modified.
            },
        ...
        ]
    }

We also overload this with the preexisting data format we were using in
/var/local/tildetown/tildetown-py/stats.py, which is of the form:

{
    'all_users': [ (array) of users on the server.
        {
            'username': (string) the username of the user.
            'default': (boolean) Is the user still using their unmodified default index.html?
            'favicon': (string) a url to an image representing the user
            },
        ...
        ]
    'num_users': (number) count of all_users
    'live_users': [ (array) an array of live users, same format as all_users. Users may appear in both arrays.
        ...
        ],
    'num_live_users': (number) count of live users
    'active_user_count': (number) count of currently logged in users
    'generated_at': (string) the time this JSON was generated in '%Y-%m-%d %H:%M:%S' format.
    'generated_at_msec': (number) the time this JSON was generated, in milliseconds since the epoch.
    'site_name': (same as 'name' above)
    'site_url': (same as 'url' above)
    'uptime': (string) output of `uptime -p`

}
Usage: tdp.py > /var/www/html/tilde.json
"""

# I suppose I could import /var/local/tildetown/tildetown-py/stats.py which
# does much of the same work, but I wanted to try to make one that needs no
# venv nor 'sh' module. (Success.) Bonus: this runs in 0.127s, vs 5.2s
# for 'stats'

# FIXME: we output quite a bit of redundant data. I think we should lose
# 'live_users' and do that filtering on the client side.

# FIXME: If we're the only consumer of the stats.py data, let's change the
# client side to use 'users' and drop 'all_users'.

import datetime
import hashlib
import json
import os
import pwd
import re
import struct
import subprocess

SYSTEM_USERS = ['wiki', 'root', 'ubuntu', 'nate', 'nobody']
DEFAULT_HTML_FILENAME = "/etc/skel/public_html/index.html"
title_re = re.compile(r'<title[^>]*>(.*)</title>', re.DOTALL)

def active_user_count():
    """Return the count of unique usernames logged in."""
    return len(set(line.split()[0] for line in
        subprocess.check_output(
            ["who"], universal_newlines=True).splitlines()))

def get_title(indexhtml):
    """Given an html file, return the content of its <title>"""
    with open(indexhtml, 'rt', errors='ignore') as fp:
        title = title_re.search(fp.read())
    if title:
        return title.group(1)

def get_users():
    """Generate tuples of the form (username, homedir) for all normal
    users on this system.

    """
    return ((p.pw_name, p.pw_dir) for p in pwd.getpwall() if
            p.pw_uid >= 1000 and
            p.pw_shell != '/bin/false' and
            p.pw_name not in SYSTEM_USERS)

def most_recent_within(path):
    """Return the most recent timestamp among all files within path, 3
    levels deep.
    """
    return max(modified_times(path), maxdepth=3)

def modified_times(path, maxdepth=None):
    """Walk the directories in path, generating timestamps for all
    files.
    """
    for root, dirs, files in os.walk(path):
        if maxdepth and len(root[len(path):].split(os.sep)) == maxdepth:
            dirs.clear()
        for f in files:
            try:
                yield os.path.getmtime(os.path.join(root, f))
            except FileNotFoundError:
                pass

def tdp_user(username, homedir):
    """Given a unix username, and their home directory, return a TDP format
    dict with information about that user.

    """
    public_html = os.path.join(homedir, 'public_html')
    index_html = os.path.join(public_html, 'index.html')
    if os.path.exists(index_html):
        return {
            'username': username,
            'title': get_title(index_html),
            'mtime': int(most_recent_within(public_html) * 1000),
            # tilde.town extensions and backward compatibility
            # FIXME: just shelling out to diff -q might be way faster than all
            # these hashes.
            'favicon': 'TODO',
            'default': subprocess.call(
                ['diff', '-q', DEFAULT_HTML_FILENAME, index_html],
                stdout=subprocess.DEVNULL) == 0,
            }
    else:
        return {
            'username': username,
            'default': False
            }

def tdp():
    now = datetime.datetime.now()
    users = [tdp_user(u, h) for u, h in get_users()]

    # TDP format data
    data = {
        'name': 'tilde.town',
        'url': 'http://tilde.town',
        'signup_url': 'http://goo.gl/forms/8IvQFTDjlo',
        'want_users': True,
        'admin_email': 'nks@lambdaphil.es',
        'description': " ".join(l.strip() for l in """
            an intentional digital community for creating and sharing works of
            art, educating peers, and technological anachronism. we are a
            completely non-commercial, donation supported, and committed to
            rejecting false technological progress in favor of empathy and
            sustainable computing.
            """.splitlines()),
        'user_count': len(users),
        'users': users,
        }

    # tilde.town extensions and backward compatibility
    data.update({
        'active_user_count': active_user_count(),
        'generated_at': now.strftime('%Y-%m-%d %H:%M:%S'),
        'generated_at_msec': int(now.timestamp() * 1000),
        'uptime': subprocess.check_output(['uptime', '-p'], universal_newlines=True),
        })
    # redundant entries we should drop after changing homepage template
    data.update({
        'all_users': data['users'],
        'num_users': data['user_count'],
        'live_users': [u for u in data['users'] if not u['default']],
        'site_name': data['name'],
        'site_url': data['url'],
        })
    data.update({
        'num_live_users': len(data['live_users']),
        })

    return data

def main():
    print(json.dumps(tdp(), sort_keys=True, indent=2))

if __name__ == '__main__':
    raise SystemExit(main())
