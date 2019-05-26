
import sys

from ..glove import (
    MB,
    Glove,
    iter_read,
    parse_glove_cooc
)


def cooc_count(args):
    glove = Glove.from_env()
    glove.cooc(
        sys.stdin.buffer,
        sys.stdout.buffer,
        vocab=args.vocab,
        memory=args.memory,
        window=args.window
    )


def cooc_shuffle(args):
    glove = Glove.from_env()
    glove.shuffle(
        sys.stdin.buffer,
        sys.stdout.buffer,
        memory=args.memory
    )


def cooc_parse(args):
    stream = iter_read(sys.stdin.buffer, MB)
    records = parse_glove_cooc(stream)
    for (source, target), weight in records:
        print('%d\t%d\t%0.6f' % (source, target, weight))
