
from .s3 import upload as corpus_upload  # noqa
from .s3 import download as corpus_download  # noqa


LIBRUSEC = 'librusec'
CORPORA = [LIBRUSEC]


def corpus_read(args):
    texts = corpus_read_(args.corpus, args.path)
    for text in texts:
        print(text)


def corpus_read_(corpus, path):
    import corus

    functions = {
        LIBRUSEC: corus.load_librusec
    }
    load = functions[corpus]
    records = load(path)
    for record in records:
        yield record.text
