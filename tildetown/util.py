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

def thread(initial, *fns):
    value = initial
    for fn in fns:
        value = fn(value)
    return value

def p(x):
    print(x)
    return x
