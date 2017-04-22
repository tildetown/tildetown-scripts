import json
import os
import pkgutil
import sys

from pystache import render

from .stats import tdp

FRONTPAGE_OUTPUT_PATH = '/var/www/tilde.town/index.html'
TDP_PATH = '/var/www/tilde.town/tilde.json'

def generate_homepage():
    """This function regenerates both our tdp json file and our homepage. It is
    intended to be called as root from the command-line."""
    template = pkgutil.get_data('tildetown', 'templates/frontpage.html')
    stats = tdp()
    frontpage_output = render(template, stats)

    with open(TDP_PATH, 'w') as f:
        f.write(json.dumps(stats))


    with open(FRONTPAGE_OUTPUT_PATH, 'w') as f:
        f.write(frontpage_output)

def mustache():
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        template = f.read()
    data = json.loads(sys.stdin.read())
    sys.stdout.write(render(template, data))
