
import numpy as np

from .record import Record


class PQ(Record):
    __attributes__ = ['vectors', 'dim', 'qdim', 'centroids', 'indexes', 'codes']

    def __init__(self, vectors, dim, qdim, centroids, indexes, codes):
        self.vectors = vectors
        self.dim = dim
        self.qdim = qdim
        self.centroids = centroids
        self.indexes = indexes
        self.codes = codes
        self.precompute()

    def precompute(self):
        # for quicker norm, sim
        self.qdims = np.arange(self.qdim)

        # codes  # qdim x centroids x -1
        # indexes  # vectors x qdim
        norm = np.sum(self.codes ** 2, axis=-1)  # qdim x centroids
        norm = np.sum(norm[self.qdims, self.indexes], axis=-1)  # vectors x 1
        self.norm = np.sqrt(norm)

        self.ab = np.matmul(
            self.codes,  # qdim x centroids x -1
            np.transpose(self.codes, axes=[0, 2, 1])  # qdim x -1 x centroids
        )  # qdim x centroids x centroids

    def sim(self, a, b):
        a_norm, b_norm = self.norm[[a, b]]
        a_index, b_index = self.indexes[[a, b]]
        ab = np.sum(self.ab[self.qdims, a_index, b_index])
        return ab / a_norm / b_norm

    def __getitem__(self, id):
        indexes = self.indexes[id]
        parts = self.codes[self.qdims, indexes]
        return parts.reshape(self.dim)

    def unpack(self):
        parts = self.codes[self.qdims, self.indexes]
        return parts.reshape(self.vectors, self.dim)

    @property
    def as_bytes(self):
        meta = self.vectors, self.dim, self.qdim, self.centroids
        meta = np.array(meta).astype(np.uint32).tobytes()
        indexes = self.indexes.astype(np.uint8).tobytes()
        codes = self.codes.astype(np.float32).tobytes()
        return meta + indexes + codes

    @classmethod
    def from_file(cls, file):
        buffer = file.read(4 * 4)
        vectors, dim, qdim, centroids = np.frombuffer(buffer, np.uint32)
        buffer = file.read(vectors * qdim)
        indexes = np.frombuffer(buffer, np.uint8).reshape(vectors, qdim)
        buffer = file.read()
        codes = np.frombuffer(buffer, np.float32).reshape(qdim, centroids, -1)
        return cls(vectors, dim, qdim, centroids, indexes, codes)


def quantize(matrix, qdim, centroids, sample, iterations):
    import pqkmeans

    encoder = pqkmeans.encoder.PQEncoder(
        iteration=iterations,
        num_subdim=qdim,
        Ks=centroids
    )

    matrix = np.array(matrix)
    vectors, dim = matrix.shape
    indexes = np.random.randint(vectors, size=sample)
    selection = matrix[indexes]

    encoder.fit(selection)
    indexes = encoder.transform(matrix)
    codes = encoder.codewords

    return PQ(vectors, dim, qdim, centroids, indexes, codes)
