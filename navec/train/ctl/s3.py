
from os.path import basename

from ..s3 import S3
from ..log import log_info


def s3_upload(args):
    key, path = args.key, args.path
    s3 = S3.from_env()
    if not key:
        key = basename(path)
    log_info('%s -> %s/%s', path, s3.bucket, key)
    s3.upload(path, key)


def s3_download(args):
    key, path = args.key, args.path
    s3 = S3.from_env()
    if not path:
        path = basename(key)
    log_info('%s/%s -> %s', s3.bucket, key, path)
    s3.download(key, path)
