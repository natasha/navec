
import torch
from torch import nn


class NavecEmbedding(nn.Module):
    def __init__(self, indexes, codes):
        super(NavecEmbedding, self).__init__()
        # same dtypes as in pq
        self.codes = torch.tensor(codes, dtype=torch.float32)
        self.indexes = torch.tensor(indexes, dtype=torch.uint8)

        subdim, centroids, self.chunk = self.codes.shape
        vectors, subdim = self.indexes.shape
        self.dim = subdim * self.chunk

        self.pad_id = vectors
        self.pad = torch.zeros(self.dim)

        # for torch.gather
        self.codes = torch.transpose(self.codes, 0, 1)  # centroids x subdim x chunk

    def forward(self, input):
        if not isinstance(input, torch.LongTensor):
            raise TypeError('expected LongTensor')

        shape = input.shape  # recover shape later
        input = input.flatten()

        mask = input == self.pad_id
        input[mask] = 0  # query first vector instead of pad_id, replace later

        # uint8 -> long
        indexes = self.indexes[input].long()  # input x subdim
        indexes = indexes.unsqueeze(-1)  # input x subdim x 1
        # for torch.gather
        indexes = indexes.expand(-1, -1, self.chunk)  # input x subdim x chunk

        output = torch.gather(self.codes, 0, indexes)  # input x subdim x chunk
        output = output.view(-1, self.dim)  # input x dim

        output[mask] = self.pad
        output = output.view(*shape, -1)

        return output


PAD = '<pad>'


class NavecVocab(object):
    def __init__(self, words):
        self.words = words + [PAD]

    def __repr__(self):
        return 'NavecVocab(words=[...])'
