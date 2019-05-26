
from navec.pq import quantize as quantize__

from ..glove import parse_glove_emb


def quantize(args):
    quantize_(args.emb, args.output, args.subdim, args.sample, args.iterations)


def quantize_(emb, output, subdim, sample, iterations):
    with open(emb) as file:
        vocab, weights = parse_glove_emb(file)
        quantize__(weights, subdim, sample, iterations)
