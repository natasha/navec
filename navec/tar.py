
import tarfile
from io import BytesIO


open_tar = tarfile.open


def write_tar(tar, bytes, filename):
    file = BytesIO(bytes)
    info = tarfile.TarInfo(filename)
    info.size = len(bytes)
    tar.addfile(tarinfo=info, fileobj=file)


def load_tar(tar, filename):
    member = tar.getmember(filename)
    return tar.extractfile(member)
