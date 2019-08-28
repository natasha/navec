
from .tar import Tar, DumpTar
from .meta import Meta
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

    def __getitem__(self, word):
        id = self.vocab[word]
        return self.pq[id]

    def __contains__(self, word):
        return word in self.vocab

    def get(self, word, default=None):
        if word in self:
            return self[word]
        return default

    def sim(self, a, b):
        a = self.vocab[a]
        b = self.vocab[b]
        return self.pq.sim(a, b)

    @property
    def as_gensim(self):
        from gensim.models import KeyedVectors

        model = KeyedVectors(self.pq.dim)
        weights = self.pq.unpack()  # warning! memory heavy
        model.add(self.vocab.words, weights)
        return model

    def sampled(self, words):
        ids = [self.vocab[_] for _ in words]
        vocab = self.vocab.sampled(words)
        pq = self.pq.sampled(ids)
        return Navec(self.meta, vocab, pq)

    def dump(self, path):
        with DumpTar(path) as tar:
            tar.dump(self.meta.as_bytes, META)
            tar.dump(self.vocab.as_bytes, VOCAB)
            tar.dump(self.pq.as_bytes, PQ_)

    @classmethod
    def load(cls, path):
        with Tar(path) as tar:
            file = tar.load(META)
            meta = Meta.from_file(file)
            Meta.check_protocol(meta.protocol)

            file = tar.load(VOCAB)
            vocab = Vocab.from_file(file)

            file = tar.load(PQ_)
            pq = PQ.from_file(file)

            return cls(meta, vocab, pq)
