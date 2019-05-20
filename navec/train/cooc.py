
import sys

from .s3 import upload as cooc_upload  # noqa
from .s3 import download as cooc_download  # noqa
from .glove import (
    Glove,
    load_stream,
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


def cooc_read(args):
    stream = load_stream(args.path, 1024 * 1024)
    records = parse_glove_cooc(stream)
    for (source, target), weight in records:
        print('%d\t%d\t%0.6f' % (source, target, weight))
