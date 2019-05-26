
import sys

from ..tokens import find_tokens


def tokenize(args):
    texts = tokenize_(sys.stdin)
    for text in texts:
        print(text)


def tokenize_(texts):
    for text in texts:
        tokens = find_tokens(text)
        text = ' '.join(tokens)
        if text:
            yield text
