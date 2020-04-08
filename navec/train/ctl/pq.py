
import sys

from navec.pq import PQ

from ..pq import (
    quantize,
    pad
)
from ..glove import (
    parse_glove_emb,
    trans_glove_emb
)
from ..log import log_info


def pq_fit(args):
    records = parse_glove_emb(sys.stdin.buffer)
    words, weights = trans_glove_emb(records)
    log_info(
        'PQ qdim: %d, centroids: %d, sample: %d, iterations: %d',
        args.qdim, args.centroids, args.sample, args.iterations
    )
    pq = quantize(weights, args.qdim, args.centroids, args.sample, args.iterations)
    sys.stdout.buffer.write(pq.as_bytes)


def pq_pad(args):
    pq = PQ.from_file(sys.stdin.buffer)
    pq = pad(pq)
    sys.stdout.buffer.write(pq.as_bytes)
