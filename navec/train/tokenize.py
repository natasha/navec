
import sys
import re


def find_tokens(text):
    text = text.lower()
    for match in re.finditer(r'[a-zа-яё-]+', text):
        token = match.group().strip('-')
        if token:  # in case just "-"
            yield token


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
