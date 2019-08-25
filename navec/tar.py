
import tarfile
from io import BytesIO

from .record import Record


class Tar(Record):
    __attributes__ = ['path']

    mode = 'r'

    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.tar = tarfile.open(self.path, self.mode)
        return self

    def __exit__(self, *args):
        self.tar.close()

    def load(self, filename):
        member = self.tar.getmember(filename)
        return self.tar.extractfile(member)


class DumpTar(Tar):
    mode = 'w'

    def dump(self, bytes, filename):
        file = BytesIO(bytes)
        info = tarfile.TarInfo(filename)
        info.size = len(bytes)
        self.tar.addfile(tarinfo=info, fileobj=file)
