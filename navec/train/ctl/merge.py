
import sys

from itertools import groupby
from heapq import (
    heappush,
    heappop,
)

from ..glove import (
    load_glove_vocab,
    format_glove_vocab,

    load_glove_cooc,
    format_glove_cooc
)


def merge_vocabs(args):
    records = merge_vocabs_(args.paths)
    lines = format_glove_vocab(records)
    sys.stdout.buffer.writelines(lines)


def merge_vocabs_(paths):
    iters = [load_glove_vocab(_) for _ in paths]
    records = merge(iters)
    return sum_groups(records)


def merge_coocs(args):
    records = merge_coocs_(args.vocab, args.pairs)
    stream = format_glove_cooc(records)
    sys.stdout.buffer.writelines(stream)


def vocab_words(records):
    for word, count in records:
        yield word


def vocab_ids(records):
    for id, (word, count) in enumerate(records):
        yield word, id


def decode_cooc(records, words):
    # in glove cooc ids start from 1
    for (source, target), weight in records:
        yield (words[source - 1], words[target - 1]), weight


def encode_cooc(records, ids):
    for (source, target), weight in records:
        yield (ids[source] + 1, ids[target] + 1), weight


def parse_pairs(pairs):
    for pair in pairs:
        yield pair.split(':', 1)


def load_decoded_cooc(cooc, vocab):
    records = load_glove_cooc(cooc)
    vocab = load_glove_vocab(vocab)
    words = list(vocab_words(vocab))
    return decode_cooc(records, words)


def merge_coocs_(vocab, pairs):
    vocab = load_glove_vocab(vocab)
    ids = dict(vocab_ids(vocab))

    pairs = parse_pairs(pairs)
    iters = [
        load_decoded_cooc(*_)
        for _ in pairs
    ]
    records = merge(iters)
    records = sum_groups(records)

    return encode_cooc(records, ids)


##########
#
#   MERGE
#
########


SENTINEL = None


def append_sentinel(items, sentinel=SENTINEL):
    for item in items:
        yield item
    yield sentinel


def merge(iters):
    iters = [append_sentinel(_) for _ in iters]
    buffer = []
    for index, records in enumerate(iters):
        key, value = next(records)
        heappush(buffer, (key, index, value))

    while buffer:
        key, index, value = heappop(buffer)
        yield key, value
        item = next(iters[index])
        if item is not SENTINEL:
            key, value = item
            heappush(buffer, (key, index, value))


def first(pair):
    return pair[0]


def second(pair):
    return pair[1]


def sum_groups(records):
    for key, group in groupby(records, first):
        count = sum(second(_) for _ in group)
        yield key, count
