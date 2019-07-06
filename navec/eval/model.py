
import os
import sys
import time

import numpy as np

from gensim.models import KeyedVectors

from navec.record import Record
from navec import Navec


W2V = 'w2v'
FASTTEXT = 'fasttext'
NAVEC = 'navec'


#########
#
#    UTILS
#
#######


def file_size(path):
    return os.stat(path).st_size


def obj_size(object):
    if isinstance(object, np.ndarray):
        return object.nbytes
    else:
        return sys.getsizeof(object)


def timeit(function, *args, **kwargs):
    start = time.time()
    result = function(*args, **kwargs)
    duration = time.time() - start
    return duration, result


########
#
#   STATS
#
#######


class Mean(Record):
    __attributes__ = ['sum', 'count']

    def __init__(self, sum=0, count=0):
        self.sum = sum
        self.count = count

    def add(self, value):
        self.sum += value
        self.count += 1

    @property
    def value(self):
        return self.sum / self.count


class Stats(Record):
    __attributes__ = ['vocab', 'disk', 'ram', 'init', 'get', 'sim']

    def __init__(self, vocab=None, disk=None, ram=None, init=None, get=None, sim=None):
        self.vocab = vocab
        self.disk = disk
        self.ram = ram

        if not init:
            init = Mean()
        self.init = init

        if not get:
            get = Mean()
        self.get = get

        if not sim:
            sim = Mean()
        self.sim = sim


#######
#
#   SCHEME
#
#######


class Scheme(Record):
    __attributes__ = ['name', 'path', 'stats']

    type = None
    tagged = False

    def __init__(self, name, path, stats=None):
        self.name = name
        self.path = path
        if not stats:
            stats = Stats()
        self.stats = stats
        self.stats.disk = self.disk

    @property
    def disk(self):
        return file_size(self.path)

    def _load(self):
        raise NotImplementedError

    def load(self):
        time, model = timeit(self._load)
        self.stats.init.add(time)
        self.stats.vocab = model.vocab
        self.stats.ram = model.ram
        return model


class RusvectoresScheme(Scheme):
    type = W2V
    tagged = True

    def _load(self):
        kv = KeyedVectors.load_word2vec_format(self.path, binary=True)
        return GensimModel(kv, self.stats)


class RusvectoresFasttextScheme(RusvectoresScheme):
    type = FASTTEXT
    tagged = False

    @property
    def paths(self):
        yield self.path
        for suffix in ['.vectors.npy', '.vectors_ngrams.npy', '.vectors_vocab.npy']:
            yield self.path + suffix

    @property
    def disk(self):
        return sum(file_size(_) for _ in self.paths)

    def _load(self):
        kv = KeyedVectors.load(self.path)
        return GensimFasttextModel(kv, self.stats)


class NavecScheme(Scheme):
    type = NAVEC

    def _load(self):
        raw = Navec.load(self.path)
        return NavecModel(raw, self.stats)


########
#
#   MODEL
#
######


class Model(object):
    ram = None
    vocab = None

    def __init__(self, stats=None):
        if not stats:
            stats = Stats()
        self.stats = stats

    def __contains__(self, word):
        raise NotImplementedError

    def _get(self, word):
        raise NotImplementedError

    def get(self, word):
        time, vector = timeit(self._get, word)
        self.stats.get.add(time)
        return vector

    def _sim(self, a, b):
        raise NotImplementedError

    def sim(self, a, b):
        time, value = timeit(self._sim, a, b)
        self.stats.sim.add(time)
        return value


class GensimModel(Model):
    def __init__(self, kv, stats=None):
        Model.__init__(self, stats)
        self.kv = kv
        self.vocab = len(kv.index2entity)
        self._sim = kv.similarity

    def __contains__(self, word):
        return word in self.kv

    def _get(self, word):
        if word in self.kv:
            return self.kv[word]

    @property
    def ram(self):
        vocab = self.kv.index2entity
        return (
            sum(obj_size(_) for _ in vocab)
            + obj_size(vocab)
            + obj_size(self.kv.vectors)
        )


class GensimFasttextModel(GensimModel):
    vocab = None

    @property
    def ram(self):
        kv = self.kv
        vocab = kv.index2entity
        return (
            sum(obj_size(_) for _ in vocab)
            + obj_size(vocab)
            + obj_size(kv.vectors)
            + obj_size(kv.vectors_vocab)
            + obj_size(kv.vectors_ngrams)
        )


class NavecModel(Model):
    def __init__(self, raw, stats=None):
        Model.__init__(self, stats)
        self.raw = raw
        self.vocab = len(raw.vocab.words)
        self._get = raw.get
        self._sim = raw.sim

    def __contains__(self, word):
        return word in self.raw

    @property
    def ram(self):
        vocab = self.raw.vocab.words
        pq = self.raw.pq
        return (
            sum(obj_size(_) for _ in vocab)
            + obj_size(vocab)
            + obj_size(pq.indexes)
            + obj_size(pq.codes)
        )
