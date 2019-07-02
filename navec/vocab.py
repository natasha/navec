
import numpy as np

from .record import Record
from .gzip import (
    compress,
    gunzip_file
)


UNK = '<unk>'


def parse_lines(lines, encoding='utf8'):
    for line in lines:
        yield line.decode(encoding).rstrip('\n')


class Vocab(Record):
    __attributes__ = ['words', 'counts']

    def __init__(self, words, counts):
        self.words = words
        self.counts = counts
        self.word_ids = {
            word: id
            for id, word in enumerate(self.words)
        }

    def __getitem__(self, word):
        return self.word_ids[word]

    def __contains__(self, word):
        return word in self.word_ids

    def __repr__(self):
        return '{name}(words=[...], counts=[...])'.format(
            name=self.__class__.__name__
        )

    def _repr_pretty_(self, printer, cycle):
        printer.text(repr(self))

    @classmethod
    def from_glove(cls, words, counts, encoding='utf8'):
        # for some reason glove vocab may have words with broken
        # unicode
        words = [_.decode(encoding, errors='ignore') for _ in words]
        return cls(words, counts)

    @property
    def as_bytes(self, encoding='utf8'):
        meta = [len(self.words)]
        meta = np.array(meta).astype(np.uint32).tobytes()

        words = '\n'.join(self.words)
        words = words.encode(encoding)

        counts = np.array(self.counts, dtype=np.uint32).tobytes()
        return compress(meta + counts + words)

    @classmethod
    def from_file(cls, file, encoding='utf8'):
        file = gunzip_file(file)

        buffer = file.read(4)
        size, = np.frombuffer(buffer, np.uint32)

        buffer = file.read(4 * size)
        counts = np.frombuffer(buffer, np.uint32).tolist()

        words = list(parse_lines(file))
        return cls(words, counts)
