
from .tar import (
    open_tar,
    write_tar,
    load_tar
)
from .meta import (
    Meta,
    VERSION
)
from .vocab import Vocab
from .pq import PQ
from .record import Record


META = 'meta.json'
VOCAB = 'vocab.bin'
PQ_ = 'pq.bin'


class Navec(Record):
    __attributes__ = ['meta', 'vocab', 'pq']

    def __init__(self, meta, vocab, pq):
        self.meta = meta
        self.vocab = vocab
        self.pq = pq

    def sim(self, a, b):
        a = self.vocab[a]
        b = self.vocab[b]
        return self.pq.sim(a, b)

    def __getitem__(self, word):
        id = self.vocab[word]
        return self.pq[id]

    def __contains__(self, word):
        return word in self.vocab

    def get(self, word, default=None):
        if word in self:
            return self[word]
        return default

    @property
    def as_gensim(self):
        from gensim.models import KeyedVectors

        model = KeyedVectors(self.pq.dim)
        weights = self.pq.unpack()  # warning! memory heavy
        model.add(self.vocab.words, weights)
        return model

    @property
    def as_torch(self):
        from .torch import NavecEmbedding

        return NavecEmbedding(
            self.pq.indexes,
            self.pq.codes
        )

    def dump(self, path):
        with open_tar(path, 'w') as tar:
            write_tar(tar, self.meta.as_bytes, META)
            write_tar(tar, self.vocab.as_bytes, VOCAB)
            write_tar(tar, self.pq.as_bytes, PQ_)

    @classmethod
    def load(cls, path):
        with open_tar(path) as tar:
            file = load_tar(tar, META)
            meta = Meta.from_file(file)
            if meta.version != VERSION:
                raise ValueError(
                    'Trying to load version %d, '
                    'only version %d is supported' % (
                        meta.version,
                        VERSION
                    )
                )

            file = load_tar(tar, VOCAB)
            vocab = Vocab.from_file(file)

            file = load_tar(tar, PQ_)
            pq = PQ.from_file(file)

            return cls(meta, vocab, pq)
