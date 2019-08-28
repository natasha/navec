
import numpy as np

import pqkmeans

from navec.pq import PQ


def quantize(matrix, qdim, centroids, sample, iterations):
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
