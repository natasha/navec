
import json
from collections import OrderedDict

from .record import Record


PROTOCOL = 1


class Meta(Record):
    __attributes__ = ['id', 'protocol']

    def __init__(self, id, protocol=PROTOCOL):
        self.id = id
        self.protocol = protocol

    def check_protocol(self):
        if self.protocol != PROTOCOL:
            raise ValueError('Expected protocol=%d, got %d' % (PROTOCOL, self.protocol))

    @property
    def as_json(self):
        return OrderedDict([
            ('id', self.id),
            ('protocol', self.protocol)
        ])

    @classmethod
    def from_json(cls, data):
        return cls(
            id=data['id'],
            protocol=data['protocol']
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
