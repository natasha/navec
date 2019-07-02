
import json
from collections import OrderedDict

from .record import Record


VERSION = 1


class Meta(Record):
    __attributes__ = ['id', 'version']

    def __init__(self, id=None, version=VERSION):
        self.id = id
        self.version = version

    @property
    def as_json(self):
        return OrderedDict([
            ('id', self.id),
            ('version', self.version)
        ])

    @classmethod
    def from_json(cls, data):
        return cls(
            id=data['id'],
            version=data['version']
        )

    @property
    def as_bytes(self):
        text = json.dumps(self.as_json, indent=2)
        return text.encode('ascii')

    @classmethod
    def from_file(cls, file):
        text = file.read().decode('ascii')
        data = json.loads(text)
        return cls.from_json(data)
