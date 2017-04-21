from json import loads
from sys import argv,stdin

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


if __name__ == '__main__':
    template = slurp(argv[1])
    data = loads(stdin.read())
    print(render(template, data))

