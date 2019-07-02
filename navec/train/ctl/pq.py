
import sys

from navec.pq import quantize

from ..glove import load_glove_emb
from ..log import log_info


def pq_fit(args):
    pq = pq_fit_(
        args.emb, args.qdim,
        args.centroids, args.sample, args.iterations
    )
    sys.stdout.buffer.write(pq.as_bytes)


def pq_fit_(emb, qdim, centroids, sample, iterations):
    log_info('Load %s', emb)
    words, weights = load_glove_emb(emb)
    log_info(
        'PQ qdim: %d, centroids: %d, sample: %d, iterations: %d',
        qdim, centroids, sample, iterations
    )
    return quantize(weights, qdim, centroids, sample, iterations)
