
from scipy.stats import spearmanr
from sklearn.metrics import average_precision_score

from navec.record import Record

from .dataset import (
    CORR,
    CLF
)


class EvalRecord(Record):
    __attributes__ = ['name', 'scores', 'stats']

    def __init__(self, name, scores, stats):
        self.name = name
        self.scores = scores
        self.stats = stats


class Score(Record):
    __attributes__ = ['value', 'support']

    def __init__(self, value, support):
        self.value = value
        self.support = support


def eval_sim_(model, pairs):
    for (a, b), etalon in pairs:
        if a in model and b in model:
            guess = model.sim(a, b)
            yield guess, etalon


def eval_sim(model, pairs):
    results = eval_sim_(model, pairs)
    guesses, etalons = zip(*results)
    return len(guesses), guesses, etalons


def eval_sim_corr(model, pairs):
    support, guesses, etalons = eval_sim(model, pairs)
    corr, p = spearmanr(guesses, etalons)
    return Score(corr, support)


def eval_sim_clf(model, pairs):
    support, guesses, etalons = eval_sim(model, pairs)
    precision = average_precision_score(etalons, guesses)
    return Score(precision, support)


def eval_model(model, datasets, tagged=False, gets=1000):
    for dataset in datasets:
        eval = None
        if dataset.type == CORR:
            eval = eval_sim_corr
        elif dataset.type == CLF:
            eval = eval_sim_clf

        pairs = dataset.pairs
        if tagged:
            pairs = dataset.tagged

        score = eval(model, pairs)
        yield dataset.name, score

        # to measure get performance
        for (a, b), _ in pairs[:gets]:
            model.get(a)


def eval_schemes(schemes, datasets):
    for scheme in schemes:
        model = scheme.load()
        scores = dict(eval_model(model, datasets, scheme.tagged))
        yield EvalRecord(
            name=scheme.name,
            scores=scores,
            stats=model.stats
        )
