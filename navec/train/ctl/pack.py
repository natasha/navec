
from navec import Navec
from navec.meta import Meta
from navec.vocab import Vocab
from navec.pq import PQ

from ..log import log_info


def pack(args):
    pack_(
        args.vocab, args.pq,
        args.id, args.version
    )


TAR = '.tar'


def open_bin(path):
    return open(path, 'rb')


def pack_(vocab, pq, id, version):
    meta = Meta(
        id=id,
        version=version
    )

    with open_bin(vocab) as file:
        vocab = Vocab.from_file(file)

    with open_bin(pq) as file:
        pq = PQ.from_file(file)

    path = id + TAR
    log_info('Dumping %s', path)
    Navec(meta, vocab, pq).dump(path)
