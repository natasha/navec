from __future__ import absolute_import

# compat with python2 which does not have gzip.compress|decompress

from gzip import GzipFile
from io import BytesIO


def compress(bytes):
    buffer = BytesIO()
    # mtime for deterministic
    with GzipFile(mode='wb', fileobj=buffer, mtime=0) as file:
        file.write(bytes)
    return buffer.getvalue()


def decompress(bytes):
    buffer = BytesIO(bytes)
    with GzipFile(mode='rb', fileobj=buffer) as file:
        return file.read()


def gunzip_file(file):
    return GzipFile(mode='rb', fileobj=file)
