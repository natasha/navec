
import sys
import argparse

from .corpus import (
    CORPORA,
    corpus_upload,
    corpus_download,
    corpus_read
)
from .tokenize import tokenize
from .vocab import (
    vocab_count,
    vocab_quantile,
    vocab_upload,
    vocab_download
)
from .cooc import (
    cooc_count,
    cooc_shuffle,
    cooc_upload,
    cooc_download
)
from .emb import (
    emb_fit,
    emb_upload,
    emb_download
)


def main():
    parser = argparse.ArgumentParser(prog='navec-train')
    parser.set_defaults(function=None)

    subs = parser.add_subparsers()

    ########
    #   CORPUS
    #########

    corpus = subs.add_parser('corpus').add_subparsers()

    sub = corpus.add_parser('upload')
    sub.set_defaults(function=corpus_upload)
    sub.add_argument('path')
    sub.add_argument('key', nargs='?')

    sub = corpus.add_parser('download')
    sub.set_defaults(function=corpus_download)
    sub.add_argument('key')
    sub.add_argument('path', nargs='?')

    sub = corpus.add_parser('read')
    sub.set_defaults(function=corpus_read)
    sub.add_argument('corpus', choices=CORPORA)
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

    sub = vocab.add_parser('upload')
    sub.set_defaults(function=vocab_upload)
    sub.add_argument('path')
    sub.add_argument('key', nargs='?')

    sub = vocab.add_parser('download')
    sub.set_defaults(function=vocab_download)
    sub.add_argument('key')
    sub.add_argument('path', nargs='?')

    ########
    #   COOC
    #######

    cooc = subs.add_parser('cooc').add_subparsers()

    sub = cooc.add_parser('count')
    sub.set_defaults(function=cooc_count)
    sub.add_argument('vocab')
    sub.add_argument('--memory', type=int, default=4)
    sub.add_argument('--window', type=int, default=10)

    sub = cooc.add_parser('shuffle')
    sub.set_defaults(function=cooc_shuffle)
    sub.add_argument('--memory', type=int, default=4)

    sub = cooc.add_parser('upload')
    sub.set_defaults(function=cooc_upload)
    sub.add_argument('path')
    sub.add_argument('key', nargs='?')

    sub = cooc.add_parser('download')
    sub.set_defaults(function=cooc_download)
    sub.add_argument('key')
    sub.add_argument('path', nargs='?')

    ########
    #   EMB
    #######

    emb = subs.add_parser('emb').add_subparsers()

    sub = emb.add_parser('fit')
    sub.set_defaults(function=emb_fit)
    sub.add_argument('cooc')
    sub.add_argument('vocab')
    sub.add_argument('output')
    sub.add_argument('--dim', type=int, default=250)
    sub.add_argument('--threads', type=int, default=4)
    sub.add_argument('--iterations', type=int, default=5)

    sub = emb.add_parser('upload')
    sub.set_defaults(function=emb_upload)
    sub.add_argument('path')
    sub.add_argument('key', nargs='?')

    sub = emb.add_parser('download')
    sub.set_defaults(function=emb_download)
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
