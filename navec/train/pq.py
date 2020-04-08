
from navec.pq import PQ


def quantize(matrix, qdim, centroids, sample, iterations):
    import numpy as np
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


def pad(pq):
    import numpy as np

    indexes, codes = pq.indexes, pq.codes
    vectors, qdim = indexes.shape
    qdim, centroids, subdim = codes.shape

    code = centroids  # assume fits into indexes.dtype

    pad = np.full(qdim, code)
    indexes = np.vstack([indexes, pad])

    pad = np.zeros((qdim, 1, subdim), dtype=codes.dtype)
    codes = np.concatenate([codes, pad], axis=1)

    return PQ(
        pq.vectors + 1, pq.dim, pq.qdim, pq.centroids + 1,
        indexes, codes
    )
