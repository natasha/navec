
from navec.pq import quantize as quantize__
from navec.vocab import Vocab
from navec import Navec

from ..glove import parse_glove_emb
from ..log import log_info


def quantize(args):
    quantize_(
        args.emb, args.output,
        args.subdim, args.centroids,
        args.sample, args.iterations,
    )


def quantize_(emb, output, subdim, centroids, sample, iterations):
    with open(emb) as file:
        log_info('Load %s', emb)
        words, weights = parse_glove_emb(file)
        log_info(
            'PQ subdim: %d, centroids: %d, sample: %d, iterations: %d',
            subdim, centroids, sample, iterations
        )
        pq = quantize__(weights, subdim, centroids, sample, iterations)
        vocab = Vocab(words)
        log_info('Dump %s', output)
        Navec(vocab, pq).dump(output)
