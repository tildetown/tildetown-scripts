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

def main(argv):
    template = slurp(argv[1])
    data = json.loads(sys.stdin.read())
    sys.stdout.write(render(template, data))

if __name__ == '__main__':
    exit(main(sys.argv))

