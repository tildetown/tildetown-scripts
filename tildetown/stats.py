import json
from functools import partial
from os import listdir
from os.path import getmtime, join
from datetime import datetime
from sh import find, uptime, who, sort, wc, cut
from tildetown.util import slurp, thread, p

# this script emits json on standard out that has information about tilde.town
# users. It denotes who has not updated their page from the default. It also
# reports the time this script was run. The user list is sorted by public_html update time.

SYSTEM_USERS = ['wiki', 'root', 'ubuntu', 'nate']

DEFAULT_HTML = slurp("/etc/skel/public_html/index.html")

username_to_html_path = lambda u: "/home/{}/public_html".format(u)

def default_p(username):
    return DEFAULT_HTML == slurp(join(username_to_html_path(username), "index.html"))

def bounded_find(path):
    # find might return 1 but still have worked fine.
    return find(path, "-maxdepth", "3", _ok_code=[0,1])

def get_active_user_count():
    return int(wc(sort(cut(who(), "-d", " ", "-f1"), "-u"), "-l"))

def guarded_mtime(path):
    try:
        return getmtime(path.rstrip())
    except Exception as _:
        return 0

def modify_time(username):
    files_to_mtimes = partial(map, guarded_mtime)
    return thread(username,
                  username_to_html_path,
                  bounded_find,
                  files_to_mtimes,
                  list,
                  max)

def sort_user_list(usernames):
    return sorted(usernames, key=modify_time)

def user_generator():
    ignore_system_users = lambda un: un not in SYSTEM_USERS
    return filter(ignore_system_users, listdir("/home"))

def get_user_data():
    username_to_data = lambda u: {'username': u,
                                  'default': default_p(u),
                                  'favicon':'TODO'}
    live_p = lambda user: not user['default']

    all_users = thread(user_generator(),
                       sort_user_list,
                       reversed,
                       partial(map, username_to_data),
                       list)

    live_users = list(filter(live_p, all_users))

    active_user_count = get_active_user_count()

    return {'all_users': all_users,
            'num_users': len(all_users),
            'num_live_users': len(live_users),
            'active_user_count': active_user_count,
            'live_users': live_users,}

def get_data():
    user_data = get_user_data()
    data = {'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'site_name': 'tilde.town',
            'site_url': 'http://tilde.town',
            'uptime': str(uptime('-p')).rstrip(),}

    data.update(user_data)
    return data

if __name__ == '__main__':
    print(json.dumps(get_data()))
