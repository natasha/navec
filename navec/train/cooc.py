
import sys
from .s3 import upload as cooc_upload  # noqa
from .s3 import download as cooc_download  # noqa
from .glove import Glove


def cooc_count(args):
    glove = Glove.from_env()
    glove.cooc(
        sys.stdin,
        sys.stdout,
        vocab=args.vocab,
        memory=args.memory,
        window=args.window
    )
