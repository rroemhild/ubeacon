from binascii import hexlify
from micropython import const


FLAGS_DATA = const(0x06)  # Discoverable, without BR/EDR support
FLAGS_TYPE = const(0x01)
FLAGS_LENGHT = const(0x02)

ADV_INTERVAL_MS = 250_000

_ADV_TYPE_NAME = const(0x09)


class Beacon:

    name = b"uBeacon"

    def __str__(self):
        adv = self.adv_bytes
        return "Bytes: {:d} data: {:s}".format(len(adv), hexlify(adv))

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self.__dict__)

    @property
    def adv_bytes(self):
        return bytes(self.adv)

    @property
    def resp(self):
        return [
            FLAGS_LENGHT,
            FLAGS_TYPE,
            FLAGS_DATA,
            len(self.name) + 1,
            _ADV_TYPE_NAME,
        ] + [x for x in self.name]

    @property
    def resp_bytes(self):
        return bytes(self.resp)

    def decode(self, adv_data):
        raise NotImplementedError("No decode method in child class implemented")
