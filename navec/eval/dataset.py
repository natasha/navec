
from navec.record import Record


CORR = 'corr'
CLF = 'clf'

SIMLEX_965 = 'simlex965'
HJ = 'hj'
RT = 'rt'
AE = 'ae'
AE2 = 'ae2'
LRWC = 'lrwc'

NOUN = 'NOUN'
ADJ = 'ADJ'
VERB = 'VERB'
POSES = {NOUN, ADJ, VERB}
POS_ALIASES = {'ADJF': ADJ}


class Dataset(Record):
    __attributes__ = ['name', 'type', 'pairs', 'tagged']

    def __init__(self, name, type, pairs, tagged):
        self.name = name
        self.type = type
        self.pairs = pairs
        self.tagged = tagged

    def __len__(self):
        return len(self.pairs)


########
#
#   TAG
#
#######


def strip_tag(word):
    word, _ = word.split('_', 1)
    return word


def strip_tags(words):
    for word in words:
        yield strip_tag(word)


def add_tag(word, tag):
    return word + '_' + tag


def noun_tagged(pairs):
    for (a, b), weight in pairs:
        a = add_tag(a, NOUN)
        b = add_tag(b, NOUN)
        yield (a, b), weight


def get_pos_analyzer():
    from pymorphy2 import MorphAnalyzer

    return MorphAnalyzer()


def get_pos(word, analyzer):
    records = analyzer.parse(word)
    for record in records:
        pos = record.tag.POS
        pos = POS_ALIASES.get(pos, pos)
        if pos in POSES:
            return pos
    return NOUN


def pos_tagged(pairs, analyzer):
    for (a, b), weight in pairs:
        pos = get_pos(a, analyzer)
        a = add_tag(a, pos)
        pos = get_pos(b, analyzer)
        b = add_tag(b, pos)
        yield (a, b), weight


########
#
#   LOAD
#
#######


def parse_score(value):
    # bool values for lrwc
    if value == 'true':
        return 1.0
    elif value == 'false':
        return 0.0
    else:
        return float(value)


def parse_pairs(lines, delimiter=',', header=True, column=2):
    if header:
        next(lines)
    for line in lines:
        row = line.rstrip().split(delimiter)
        a, b = row[:2]
        score = parse_score(row[column])
        yield (a, b), score


def load_pairs(path, **kwargs):
    with open(path) as file:
        for record in parse_pairs(file, **kwargs):
            yield record
