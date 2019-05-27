
import gzip

from .record import Record


class Vocab(Record):
    __attributes__ = ['words']

    def __init__(self, words):
        self.words = words
        self.word_ids = {
            word: id
            for id, word in enumerate(words)
        }

    def __getitem__(self, word):
        return self.word_ids[word]

    def __contains__(self, word):
        return word in self.word_ids

    @property
    def as_bytes(self, encoding='utf8'):
        text = '\n'.join(self.words)
        bytes = text.encode(encoding)
        return gzip.compress(bytes)

    @classmethod
    def load(cls, file, encoding='utf8'):
        data = file.read()
        bytes = gzip.decompress(data)
        text = bytes.decode(encoding)
        words = text.splitlines()
        return cls(words)
