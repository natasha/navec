

class Vocab(object):
    def __init__(self, words):
        self.words = words
        self.word_ids = {
            word: id
            for id, word in enumerate(words)
        }

    @property
    def as_bytes(self, encoding='utf8'):
        buffer = b''
        for index, word in enumerate(self.words):
            if index > 0:
                buffer += b'\n'
            buffer += word.encode(encoding)
        return buffer

    @classmethod
    def load(cls, file, encoding='utf8'):
        words = []
        for line in file:
            word = line.decode(encoding).rstrip('\n')
            words.append(word)
        return cls(words)
