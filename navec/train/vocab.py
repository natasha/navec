
import sys

from .s3 import upload as vocab_upload  # noqa
from .s3 import download as vocab_download  # noqa
from .glove import (
    Glove,
    parse_glove_vocab
)


def vocab_count(args):
    glove = Glove.from_env()
    glove.vocab(sys.stdin, sys.stdout)


def vocab_quantile(args):
    count = vocab_quantile_(sys.stdin, args.share)
    print(count)


def vocab_quantile_(lines, share):
    records = parse_glove_vocab(lines)
    counts = [count for _, count in records]
    total = sum(counts)
    accumulator = 0
    counts = sorted(counts, reverse=True)
    for index, count in enumerate(counts):
        if accumulator / total >= share:
            return index
        accumulator += count
    return len(counts)
