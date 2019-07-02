
from os import environ as env
from os.path import (
    join as join_path,
    splitext as split_extension
)
from subprocess import (
    DEVNULL,
    PIPE,
    Popen,
    check_call
)
from struct import (
    calcsize,
    pack,
    iter_unpack
)
from tempfile import TemporaryDirectory


COOC_RECORD = 'iid'
COOC_RECORD_SIZE = calcsize(COOC_RECORD)


class Glove:
    def __init__(self, dir):
        self.dir = dir

    @classmethod
    def from_env(cls):
        dir = env['GLOVE_DIR']
        return cls(dir)

    def vocab(self, *args, **kwargs):
        bin = join_path(self.dir, 'vocab_count')
        return glove_vocab(bin, *args, **kwargs)

    def cooc(self, *args, **kwargs):
        bin = join_path(self.dir, 'cooccur')
        return glove_cooc(bin, *args, **kwargs)

    def shuffle(self, *args, **kwargs):
        bin = join_path(self.dir, 'shuffle')
        return glove_shuffle(bin, *args, **kwargs)

    def emb(self, *args, **kwargs):
        bin = join_path(self.dir, 'glove')
        return glove_emb(bin, *args, **kwargs)


########
#
#   VOCAB
#
#######


def read_glove_vocab(path):
    with open(path, 'rb') as file:
        for line in file:
            yield line


def parse_glove_vocab(lines):
    for line in lines:
        word, count = line.split(None, 1)
        count = int(count)
        yield word, count


def format_glove_vocab(records):
    for word, count in records:
        yield b'%s %d\n' % (word, count)


def load_glove_vocab(path):
    lines = read_glove_vocab(path)
    return parse_glove_vocab(lines)


def trans_glove_vocab(records):
    words, counts = [], []
    for word, count in records:
        words.append(word)
        counts.append(count)
    return words, counts


def glove_vocab(bin, input, output, min_count=1):
    command = [
        bin,
        '-min-count', str(min_count),
        '-verbose', '0'
    ]
    check_call(command, stdin=input, stdout=output, stderr=DEVNULL)


##########
#
#   COOC
#
########


KB = 1024
MB = 1024 * KB


def iter_read(file, size):
    while True:
        chunk = file.read(size)
        if not chunk:
            break
        yield chunk


def read_chunks(path, size):
    with open(path, 'rb') as file:
        for chunk in iter_read(file, size):
            yield chunk


def parse_glove_cooc(stream, format=COOC_RECORD):
    for chunk in stream:
        for source, target, weight in iter_unpack(format, chunk):
            yield (source, target), weight


def load_glove_cooc(path, size=MB, format=COOC_RECORD):
    stream = read_chunks(path, size)
    return parse_glove_cooc(stream, format)


def format_glove_cooc(records, format=COOC_RECORD):
    for (source, target), weight in records:
        chunk = pack(format, source, target, weight)
        yield chunk


def glove_cooc(bin, input, output, vocab, memory, window):
    with TemporaryDirectory(prefix='cooc_') as dir:
        command = [
            bin,
            '-vocab-file', vocab,
            '-overflow-file', join_path(dir, 'overflow'),
            '-memory', str(memory),
            '-window-size', str(window),
            '-verbose', '0'
        ]
        check_call(command, stdin=input, stdout=output, stderr=DEVNULL)


#########
#
#   SHUFFLE
#
#######


def glove_shuffle(bin, input, output, memory):
    with TemporaryDirectory(prefix='shuf_') as dir:
        command = [
            bin,
            '-temp-file', join_path(dir, 'shuf'),
            '-memory', str(memory),
            '-verbose', '0',
        ]
        check_call(command, stdin=input, stdout=output, stderr=DEVNULL)


#########
#
#   EMB
#
#########


def parse_log(lines):
    for line in lines:
        yield line.decode('ascii').rstrip('\n')


def glove_emb(bin, cooc, vocab, output, dim, threads, iterations):
    prefix, _ = split_extension(output)
    command = [
        bin,
        '-input-file', cooc,
        '-save-file', prefix,
        '-vocab-file', vocab,

        '-vector-size', str(dim),
        '-threads', str(threads),
        '-iter', str(iterations),

        '-binary', '0',  # txt output
        '-verbose', '2'
    ]
    with Popen(command, stderr=PIPE) as process:
        log = parse_log(process.stderr)
        for line in log:
            yield line


def read_glove_emb(path):
    with open(path) as file:
        for line in file:
            yield line.rstrip()


def parse_glove_emb(lines):
    for line in lines:
        parts = line.split()
        word, vector = parts[0], parts[1:]
        vector = [float(_) for _ in vector]
        yield word, vector


def trans_glove_emb(records):
    words, weights = [], []
    for word, vector in records:
        words.append(word)
        weights.append(vector)
    return words, weights


def load_glove_emb(path):
    lines = read_glove_emb(path)
    records = parse_glove_emb(lines)
    words, weights = trans_glove_emb(records)
    return words, weights
