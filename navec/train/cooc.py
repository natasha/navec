
import sys

from .s3 import upload as cooc_upload  # noqa
from .s3 import download as cooc_download  # noqa
from .glove import Glove


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
