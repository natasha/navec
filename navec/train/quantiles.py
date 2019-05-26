

SHARES = [
    0.5, 0.6, 0.7, 0.8, 0.9,
    0.91, 0.92, 0.93, 0.94,
    0.95, 0.96, 0.97, 0.98,
    0.99, 1.0
]


def pop(items):
    return items[0], items[1:]


def get_quantiles(records, shares=SHARES):
    if not shares:
        return

    counts = [count for _, count in records]

    total = sum(counts)
    accumulator = 0

    shares = sorted(shares)
    share, shares = pop(shares)

    counts = sorted(counts, reverse=True)
    for index, count in enumerate(counts):
        accumulator += count
        if accumulator / total >= share:
            yield share, index
            if not shares:
                break
            share, shares = pop(shares)
