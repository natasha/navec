
import sys

from navec.pq import quantize

from ..glove import (
    parse_glove_emb,
    trans_glove_emb
)
from ..log import log_info


def pq_fit(args):
    records = parse_glove_emb(sys.stdin.buffer)
    pq = pq_fit_(
        records, args.qdim,
        args.centroids, args.sample, args.iterations
    )
    sys.stdout.buffer.write(pq.as_bytes)


def pq_fit_(records, qdim, centroids, sample, iterations):
    words, weights = trans_glove_emb(records)
    log_info(
        'PQ qdim: %d, centroids: %d, sample: %d, iterations: %d',
        qdim, centroids, sample, iterations
    )
    return quantize(weights, qdim, centroids, sample, iterations)
