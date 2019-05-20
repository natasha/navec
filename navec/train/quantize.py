
from navec.pq import (
    PQ,
    dump_pq
)

from .io import load_lines
from .glove import parse_glove_emb


def quantize(args):
    quantize_(args.emb, args.output, args.subdim, args.sample, args.iterations)


def quantize_(emb, output, subdim, sample, iterations):
    lines = load_lines(emb)
    vocab, weights = parse_glove_emb(lines)
    model = quantize__(vocab, weights, subdim, sample, iterations)
    dump_pq(model, output)


def quantize__(vocab, weights, subdim, sample, iterations, centroids=256):
    import pqkmeans
    import numpy as np

    encoder = pqkmeans.encoder.PQEncoder(
        iteration=iterations,
        num_subdim=subdim,
        Ks=centroids
    )

    weights = np.array(weights)
    size, dim = weights.shape

    indexes = np.random.randint(size, size=sample)
    selection = weights[indexes]

    encoder.fit(selection)
    indexes = encoder.transform(weights)
    codes = encoder.codewords

    return PQ(dim, subdim, centroids, vocab, indexes, codes)
