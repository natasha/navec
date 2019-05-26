
from ..log import log_info
from ..glove import Glove


def emb_fit(args):
    glove = Glove.from_env()
    log = glove.emb(
        args.cooc,
        args.vocab,
        args.output,
        args.dim,
        args.threads,
        args.iterations
    )
    for line in log:
        log_info(line)
