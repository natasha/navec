
import tarfile
from io import BytesIO

import numpy as np


def word_ids(vocab):
    for id, word in enumerate(vocab):
        yield word, id


PQ_VOCAB = 'vocab.txt'
PQ_DATA = 'data.bin'


class PQ:
    def __init__(self, dim, subdim, centroids, vocab, indexes, codes):
        self.dim = dim
        self.subdim = subdim
        self.centroids = centroids
        self.vocab = vocab
        self.indexes = indexes
        self.codes = codes
        self.precompute()

    def precompute(self):
        self.word_ids = dict(word_ids(self.vocab))
        # for quicker l2, query_pq
        self.subdim_index = np.arange(self.subdim)

        # codes  # subdim x centroids x -1
        # indexes  # vocab x subdim
        l2 = np.sum(self.codes ** 2, axis=-1)  # subdim x centroids
        l2 = np.sum(l2[self.subdim_index, self.indexes], axis=-1)  # vocab x 1
        self.l2 = np.sqrt(l2)

        self.ab = np.matmul(
            self.codes,  # subdim x centroids x -1
            np.transpose(self.codes, axes=[0, 2, 1])  # subdim x -1 x centroids
        )  # subdim x centroids x centroids

    def sim(self, a, b):
        a_id = self.word_ids[a]
        b_id = self.word_ids[b]
        a_l2, b_l2 = self.l2[[a_id, b_id]]
        a_index, b_index = self.indexes[[a_id, b_id]]
        ab = np.sum(self.ab[self.subdim_index, a_index, b_index])
        return ab / a_l2 / b_l2


def format_pq_vocab(vocab, encoding='utf8'):
    return b'\n'.join(
        _.encode(encoding)
        for _ in vocab
    )


def format_pq_data(model):
    meta = np.array([
        len(model.vocab),
        model.dim,
        model.subdim,
        model.centroids
    ]).astype(np.uint32)
    indexes = model.indexes.astype(np.uint8)
    codes = model.codes.astype(np.float32)
    return meta.tobytes() + indexes.tobytes() + codes.tobytes()


def write_tar(tar, data, filename):
    file = BytesIO(data)
    info = tarfile.TarInfo(filename)
    info.size = len(data)
    tar.addfile(tarinfo=info, fileobj=file)


def dump_pq(model, path):
    with tarfile.open(path, 'w') as tar:
        data = format_pq_vocab(model.vocab)
        write_tar(tar, data, PQ_VOCAB)

        data = format_pq_data(model)
        write_tar(tar, data, PQ_DATA)


def parse_pq_vocab(file, encoding='utf8'):
    for line in file:
        yield line.decode(encoding).rstrip('\n')


def parse_pq_data(file):
    buffer = file.read(4 * 4)
    vocab, dim, subdim, centroids = np.frombuffer(buffer, np.uint32)

    buffer = file.read(vocab * subdim)
    indexes = np.frombuffer(buffer, np.uint8).reshape(vocab, subdim)

    buffer = file.read()
    codes = np.frombuffer(buffer, np.float32).reshape(subdim, centroids, -1)

    return dim, subdim, centroids, indexes, codes


def load_pq(path):
    with tarfile.open(path) as tar:
        file = tar.extractfile(PQ_VOCAB)
        vocab = list(parse_pq_vocab(file))

        file = tar.extractfile(PQ_DATA)
        dim, subdim, centroids, indexes, codes = parse_pq_data(file)

        return PQ(
            dim,
            subdim,
            centroids,
            vocab,
            indexes,
            codes
        )
