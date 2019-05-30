
import pandas as pd


def format_mb(bytes):
    mb = bytes / 1024 / 1024
    return '%0.1f' % mb


def format_sec(secs):
    return '%0.1f' % secs


def format_mks(secs):
    mks = secs * 1000000
    return '%0.1f' % mks


def report_table(records, schemes, datasets):
    data = []
    names = [_.name for _ in datasets]
    for record in records:
        row = [
            record.name,
            format_sec(record.stats.init.value),
            format_mks(record.stats.get.value),
            format_mb(record.stats.disk),
            format_mb(record.stats.ram)
        ]
        for name in names:
            score = record.scores[name]
            row.append('%0.3f | %d' % (score.value, score.support))
        data.append(row)

    table = pd.DataFrame(
        data,
        columns=['model', 'init, s', 'get, µs', 'disk, mb', 'ram, mb'] + names
    )
    table = table.set_index('model')
    names = [_.name for _ in schemes]
    table = table.reindex(index=names)
    return table
