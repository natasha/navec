
import sys

from navec.vocab import Vocab

from ..glove import (
    Glove,
    parse_glove_vocab,
    format_glove_vocab,
    trans_glove_vocab
)
from ..quantiles import get_quantiles


def vocab_count(args):
    glove = Glove.from_env()
    glove.vocab(sys.stdin.buffer, sys.stdout.buffer)


def vocab_quantile(args):
    records = parse_glove_vocab(sys.stdin.buffer)
    quantiles = get_quantiles(records)
    for share, index in quantiles:
        print('%0.3f\t%d' % (share, index))


def vocab_pack(args):
    records = parse_glove_vocab(sys.stdin.buffer)
    words, counts = trans_glove_vocab(records)
    vocab = Vocab.from_glove(words, counts)
    sys.stdout.buffer.write(vocab.as_bytes)


def vocab_unpack(args):
    vocab = Vocab.from_file(sys.stdin.buffer)
    lines = format_glove_vocab(vocab.as_glove)
    sys.stdout.buffer.writelines(lines)
