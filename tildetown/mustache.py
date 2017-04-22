#!/usr/bin/env python3
import json
import sys

from pystache import render

def slurp(file_path):
    contents = None
    try:
        with open(file_path, 'r', encoding="utf-8") as f:
            contents = f.read()
    except FileNotFoundError:
        pass
    except UnicodeDecodeError:
        pass
    return contents

# when you install scripts with entry_points in a setup.py, the resulting
# executable just calls main() and you have to look up sys.argv yourself. I like to explicitly take an argv in my actual main, hence the weird indirection. could probably be better.
def _main(argv):
    template = slurp(argv[1])
    data = json.loads(sys.stdin.read())
    sys.stdout.write(render(template, data))

def main():
    _main(sys.argv)

if __name__ == '__main__':
    exit(_main(sys.argv))

