
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


def eval_sim(model, pairs, default=0):
    etalons = []
    guesses = []
    for (a, b), etalon in pairs:
        etalons.append(etalon)

        # measure get speed
        model.get(a)

        if a in model and b in model:
            guess = model.sim(a, b)
        else:
            guess = default

        guesses.append(guess)
    return guesses, etalons


def eval_sim_corr(model, pairs):
    guesses, etalons = eval_sim(model, pairs)
    corr, p = spearmanr(guesses, etalons)
    return corr


def eval_sim_clf(model, pairs):
    guesses, etalons = eval_sim(model, pairs)
    return average_precision_score(etalons, guesses)


def eval_model(model, datasets, tagged=False):
    for dataset in datasets:
        function = None
        if dataset.type == CORR:
            function = eval_sim_corr
        elif dataset.type == CLF:
            function = eval_sim_clf

        pairs = dataset.pairs
        if tagged:
            pairs = dataset.tagged

        score = function(model, pairs)
        yield dataset.name, score


def eval_schemes(schemes, datasets):
    for scheme in schemes:
        model = scheme.load()
        scores = dict(eval_model(model, datasets, scheme.tagged))
        yield EvalRecord(
            name=scheme.name,
            scores=scores,
            stats=model.stats
        )
