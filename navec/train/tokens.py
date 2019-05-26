
import re


def find_tokens(text):
    text = text.lower()
    for match in re.finditer(r'[a-zа-яё-]+', text):
        token = match.group().strip('-')
        if token:  # in case just "-"
            yield token
