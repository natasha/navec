
import sys

from ..glove import (
    Glove,
    parse_glove_vocab
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
