import json
import sys

from pystache import render


def mustache():
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        template = f.read()
    data = json.loads(sys.stdin.read())
    sys.stdout.write(render(template, data))
