
from navec.pq import quantize
from navec.vocab import Vocab
from navec import Navec

from ..glove import load_glove_emb
from ..log import log_info


def quant_fit(args):
    quant_fit_(
        args.emb, args.output,
        args.subdim, args.centroids,
        args.sample, args.iterations,
    )


def quant_fit_(emb, output, subdim, centroids, sample, iterations):
    log_info('Load %s', emb)
    words, weights = load_glove_emb(emb)
    log_info(
        'PQ subdim: %d, centroids: %d, sample: %d, iterations: %d',
        subdim, centroids, sample, iterations
    )
    pq = quantize(weights, subdim, centroids, sample, iterations)
    vocab = Vocab(words)
    log_info('Dump %s', output)
    Navec(vocab, pq).dump(output)
