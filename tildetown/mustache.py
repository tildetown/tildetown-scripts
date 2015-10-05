from json import loads
from sys import argv,stdin

from pystache import render

from tildetown.util import slurp

if __name__ == '__main__':
    template = slurp(argv[1])
    data = loads(stdin.read())
    print(render(template, data))

