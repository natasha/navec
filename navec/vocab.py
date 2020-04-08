
from gzip import (
    compress,
    GzipFile
)

import numpy as np

from .record import Record


UNK = '<unk>'
PAD = '<pad>'


class Vocab(Record):
    __attributes__ = ['words', 'counts']

    def __init__(self, words, counts):
        self.words = words
        self.counts = counts
        self.word_ids = {
            word: id
            for id, word in enumerate(self.words)
        }
        self.unk_id = self.word_ids.get(UNK)
        self.pad_id = self.word_ids.get(PAD)

    def __getitem__(self, word):
        return self.word_ids[word]

    def __contains__(self, word):
        return word in self.word_ids

    def get(self, word, default=None):
        if word in self:
            return self[word]
        return default

    def count(self, word):
        return self.counts[self.word_ids[word]]

    def top(self, count=None):
        return sorted(
            self.words,
            key=self.count,
            reverse=True
        )[:count]

    def sampled(self, words):
        words = list(words)
        counts = [
            self.counts[self.word_ids[_]]
            for _ in words
        ]
        return Vocab(words, counts)

    def __repr__(self):
        return '{name}(words=[...], counts=[...])'.format(
            name=self.__class__.__name__
        )

    def _repr_pretty_(self, printer, cycle):
        printer.text(repr(self))

    @classmethod
    def from_glove(cls, words, counts):
        # for some reason glove vocab may have words with broken
        # unicode
        words = [_.decode('utf8', errors='ignore') for _ in words]

        # emb has unk in the end
        for word in (UNK, PAD):
            words.append(word)
            counts.append(0)

        return cls(words, counts)

    @property
    def as_glove(self):
        for word, count in zip(self.words, self.counts):
            if word in (UNK, PAD):
                continue
            word = word.encode('utf8')
            yield word, count

    @property
    def as_bytes(self):
        meta = [len(self.counts)]
        meta = np.array(meta).astype(np.uint32).tobytes()

        words = '\n'.join(self.words)
        words = words.encode('utf8')

        counts = np.array(self.counts, dtype=np.uint32).tobytes()
        return compress(meta + counts + words)

    @classmethod
    def from_file(cls, file):
        file = GzipFile(mode='rb', fileobj=file)

        buffer = file.read(4)
        size, = np.frombuffer(buffer, np.uint32)

        buffer = file.read(4 * size)
        counts = np.frombuffer(buffer, np.uint32).tolist()

        text = file.read().decode('utf8')
        words = text.splitlines()

        return cls(words, counts)
