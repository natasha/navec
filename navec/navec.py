
from .tar import (
    open_tar,
    write_tar,
    load_tar
)
from .pq import PQ
from .vocab import Vocab


VOCAB = 'vocab.txt'
PQ_ = 'pq.bin'


class Navec(object):
    def __init__(self, vocab, pq):
        self.vocab = vocab
        self.pq = pq

    def dump(self, path):
        with open_tar(path, 'w') as tar:
            write_tar(tar, self.vocab.as_bytes, VOCAB)
            write_tar(tar, self.pq.as_bytes, PQ_)

    @classmethod
    def load(cls, path):
        with open_tar(path) as tar:
            file = load_tar(tar, VOCAB)
            vocab = Vocab.load(file)
            file = load_tar(tar, PQ)
            pq = PQ.load(file)
            return cls(vocab, pq)
