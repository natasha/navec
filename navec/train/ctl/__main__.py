
import sys
import argparse

from .corpus import (
    CORPORA,
    corpus_read
)
from .tokenize import tokenize
from .vocab import (
    vocab_count,
    vocab_quantile
)
from .cooc import (
    cooc_count,
    cooc_shuffle,
    cooc_parse
)
from .emb import emb_fit
from .quantize import quantize
from .s3 import (
    s3_upload,
    s3_download
)


def main():
    parser = argparse.ArgumentParser(prog='navec-train')
    parser.set_defaults(function=None)

    subs = parser.add_subparsers()

    ########
    #   CORPUS
    #########

    sub = subs.add_parser('corpus')
    sub.set_defaults(function=corpus_read)
    sub.add_argument('name', choices=CORPORA)
    sub.add_argument('path')

    ########
    #  TOKENIZE
    #######

    sub = subs.add_parser('tokenize')
    sub.set_defaults(function=tokenize)

    ########
    #   VOCAB
    #######

    vocab = subs.add_parser('vocab').add_subparsers()

    sub = vocab.add_parser('count')
    sub.set_defaults(function=vocab_count)

    sub = vocab.add_parser('quantile')
    sub.set_defaults(function=vocab_quantile)

    ########
    #   COOC
    #######

    cooc = subs.add_parser('cooc').add_subparsers()

    sub = cooc.add_parser('count')
    sub.set_defaults(function=cooc_count)
    sub.add_argument('vocab')
    sub.add_argument('--memory', type=int, default=4)
    sub.add_argument('--window', type=int, default=10)

    sub = cooc.add_parser('parse')
    sub.set_defaults(function=cooc_parse)

    sub = cooc.add_parser('shuffle')
    sub.set_defaults(function=cooc_shuffle)
    sub.add_argument('--memory', type=int, default=4)

    ########
    #   EMB
    #######

    sub = subs.add_parser('emb')
    sub.set_defaults(function=emb_fit)
    sub.add_argument('cooc')
    sub.add_argument('vocab')
    sub.add_argument('output')
    sub.add_argument('--dim', type=int, default=250)
    sub.add_argument('--threads', type=int, default=4)
    sub.add_argument('--iterations', type=int, default=5)

    #########
    #   QUANTIZE
    ########

    sub = subs.add_parser('quantize')
    sub.set_defaults(function=quantize)
    sub.add_argument('emb')
    sub.add_argument('output')
    sub.add_argument('subdim', type=int)
    sub.add_argument('--centroids', type=int, default=255)  # one for pad vector
    sub.add_argument('--sample', type=int, default=10000)
    sub.add_argument('--iterations', type=int, default=50)

    ######
    #   S3
    #######

    s3 = subs.add_parser('s3').add_subparsers()

    sub = s3.add_parser('upload')
    sub.set_defaults(function=s3_upload)
    sub.add_argument('path')
    sub.add_argument('key', nargs='?')

    sub = s3.add_parser('download')
    sub.set_defaults(function=s3_download)
    sub.add_argument('key')
    sub.add_argument('path', nargs='?')

    ##########
    #   PARSE
    ########

    args = sys.argv[1:]
    args = parser.parse_args(args)
    if not args.function:
        parser.print_help()
        parser.exit()
    try:
        args.function(args)
    except (KeyboardInterrupt, BrokenPipeError):
        pass
