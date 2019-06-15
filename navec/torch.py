
import numpy as np

import torch
from torch import nn


PAD = '<pad>'


class NavecEmbedding(nn.Module):
    def __init__(self, indexes, codes):
        super(NavecEmbedding, self).__init__()

        vectors, subdim = indexes.shape
        subdim, centroids, chunk = codes.shape
        self.chunk = chunk
        self.dim = subdim * chunk

        # add pad, assume centroids <= 255, so that pad_indexes fits
        # into bytes
        self.pad_id = vectors
        pad_indexes = np.full((1, subdim), centroids)
        pad_codes = np.zeros((subdim, 1, chunk))
        indexes = np.vstack([indexes, pad_indexes])
        codes = np.hstack([codes, pad_codes])
        
        # same dtypes as in pq
        indexes = torch.tensor(indexes, dtype=torch.uint8)
        codes = torch.tensor(codes, dtype=torch.float32)

        # for torch.gather
        codes = codes.transpose(0, 1)  # centroids x subdim x chunk

        self.codes = nn.Parameter(codes, requires_grad=False)
        self.indexes = nn.Parameter(indexes, requires_grad=False)

    def extra_repr(self):
        return 'indexes=[...], codes=[...]'

    def forward(self, input):
        if not isinstance(input, torch.LongTensor):
            raise TypeError('expected LongTensor')

        shape = input.shape  # recover shape later
        input = input.flatten()

        # uint8 -> long
        indexes = self.indexes[input].long()  # input x subdim
        # for torch.gather
        indexes = indexes.unsqueeze(-1)  # input x subdim x 1
        indexes = indexes.expand(-1, -1, self.chunk)  # input x subdim x chunk

        output = torch.gather(self.codes, 0, indexes)  # input x subdim x chunk
        output = output.view(*shape, self.dim)  # input x dim

        return output


class NavecVocab(object):
    def __init__(self, words):
        self.words = words + [PAD]

    def __repr__(self):
        return 'NavecVocab(words=[...])'
