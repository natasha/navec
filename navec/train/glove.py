
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


def parse_glove_vocab(lines):
    for line in lines:
        token, count = line.split(None, 1)
        count = int(count)
        yield token, count


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


def parse_glove_cooc(stream, format=COOC_RECORD):
    for chunk in stream:
        for source, target, weight in iter_unpack(format, chunk):
            yield (source, target), weight


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


def glove_emb(bin, input, output, vocab, dim, threads, iterations):
    prefix, _ = split_extension(output)
    command = [
        bin,
        '-input-file', input,
        '-save-file', prefix,
        '-vocab-file', vocab,

        '-vector-size', str(dim),
        '-threads', str(threads),
        '-iter', str(iterations),

        '-binary', '0',  # txt output
        '-verbose', '2'
    ]
    with Popen(command, stderr=PIPE) as process:
        for line in process.stderr:
            yield line
