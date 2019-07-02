
import numpy as np

import torch
from torch import nn


class NavecEmbedding(nn.Module):
    def __init__(self, indexes, codes):
        super(NavecEmbedding, self).__init__()

        vectors, qdim = indexes.shape
        qdim, centroids, chunk = codes.shape
        self.chunk = chunk
        self.dim = qdim * chunk

        # add pad, assume centroids <= 255, so that pad_indexes fit
        # into bytes
        self.pad_id = vectors
        pad_indexes = np.full((1, qdim), centroids)
        pad_codes = np.zeros((qdim, 1, chunk))
        indexes = np.vstack([indexes, pad_indexes])
        codes = np.hstack([codes, pad_codes])

        # same dtypes as in pq
        indexes = torch.tensor(indexes, dtype=torch.uint8)
        codes = torch.tensor(codes, dtype=torch.float32)

        # for torch.gather
        codes = codes.transpose(0, 1)  # centroids x qdim x chunk

        self.codes = nn.Parameter(codes, requires_grad=False)
        self.indexes = nn.Parameter(indexes, requires_grad=False)

    def extra_repr(self):
        return 'indexes=[...], codes=[...]'

    def forward(self, input):
        shape = input.shape  # recover shape later
        input = input.flatten()

        # uint8 -> long
        indexes = self.indexes[input].long()  # input x qdim
        # for torch.gather
        indexes = indexes.unsqueeze(-1)  # input x qdim x 1
        indexes = indexes.expand(-1, -1, self.chunk)  # input x qdim x chunk

        output = torch.gather(self.codes, 0, indexes)  # input x qdim x chunk
        shape = shape + (self.dim,)
        output = output.view(*shape)  # input x dim

        return output
