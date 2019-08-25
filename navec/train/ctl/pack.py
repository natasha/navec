
from navec import Navec
from navec.meta import Meta
from navec.vocab import Vocab
from navec.pq import PQ

from ..log import log_info


def pack(args):
    pack_(
        args.vocab, args.pq,
        args.id
    )


def open_bin(path):
    return open(path, 'rb')


def pack_(vocab, pq, id):
    meta = Meta(id)

    with open_bin(vocab) as file:
        vocab = Vocab.from_file(file)

    with open_bin(pq) as file:
        pq = PQ.from_file(file)

    path = 'navec_%s.tar' % id
    log_info('Dumping %s', path)
    Navec(meta, vocab, pq).dump(path)
