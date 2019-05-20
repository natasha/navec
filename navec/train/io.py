

KB = 1024
MB = 1024 * KB


def iter_read(file, size):
    while True:
        chunk = file.read(size)
        if not chunk:
            break
        yield chunk


def load_lines(path):
    with open(path) as file:
        for line in file:
            yield line.rstrip('\n')
