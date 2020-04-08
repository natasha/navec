
from navec import Navec
from navec.meta import Meta
from navec.vocab import Vocab
from navec.pq import PQ

from ..log import log_info


def open_bin(path):
    return open(path, 'rb')


def pack(args):
    meta = Meta(args.id)

    with open_bin(args.vocab) as file:
        vocab = Vocab.from_file(file)

    with open_bin(args.pq) as file:
        pq = PQ.from_file(file)

    path = 'navec_%s.tar' % args.id
    log_info('Dumping %s', path)
    Navec(meta, vocab, pq).dump(path)
