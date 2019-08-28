
import json
from collections import OrderedDict

from .record import Record


class Meta(Record):
    __attributes__ = ['id', 'protocol']

    PROTOCOL = 1

    def __init__(self, id, protocol=PROTOCOL):
        self.id = id
        self.protocol = protocol

    @property
    def as_json(self):
        return OrderedDict([
            ('id', self.id),
            ('protocol', self.protocol)
        ])

    @classmethod
    def check_protocol(cls, protocol):
        if protocol != cls.PROTOCOL:
            raise ValueError('Expected protocol=%d, got %d' % (cls.PROTOCOL, protocol))

    @classmethod
    def from_json(cls, data):
        protocol = data.get('protocol')
        cls.check_protocol(protocol)
        return cls(
            id=data['id'],
            protocol=protocol
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
