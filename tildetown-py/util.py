def slurp(file_path):
    contents = None
    with open(file_path, 'r') as f:
        contents = f.read()
    return contents

def thread(initial, *fns):
    value = initial
    for fn in fns:
        value = fn(value)
    return value
