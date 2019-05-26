
import tarfile
from io import BytesIO


def write_tar(tar, bytes, filename):
    file = BytesIO(bytes)
    info = tarfile.TarInfo(filename)
    info.size = len(bytes)
    tar.addfile(tarinfo=info, fileobj=file)
