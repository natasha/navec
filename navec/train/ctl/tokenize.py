
import sys

from ..tokens import find_tokens


def tokenize(args):
    for text in sys.stdin:
        tokens = find_tokens(text)
        text = ' '.join(tokens)
        if text:
            print(text)
