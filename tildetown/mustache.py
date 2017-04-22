#!/usr/bin/env python3
import json
import sys

from pystache import render

# when you install scripts with entry_points in a setup.py, the resulting
# executable just calls main() and you have to look up sys.argv yourself. I
# like to explicitly take an argv in my actual main, hence the weird
# indirection. could probably be better.
def _main(argv):
    with open(argv[1], 'r', encoding='utf-8') as f:
        template = f.read()
    data = json.loads(sys.stdin.read())
    sys.stdout.write(render(template, data))

def main():
    _main(sys.argv)

if __name__ == '__main__':
    exit(_main(sys.argv))

