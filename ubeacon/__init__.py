import bluetooth

from binascii import hexlify
from micropython import const


FLAGS_DATA = const(0x06)  # Discoverable, without BR/EDR support
FLAGS_TYPE = const(0x01)
FLAGS_LENGHT = const(0x02)

_ADV_TYPE_NAME = const(0x09)
_ADV_INTERVAL_MS = 250_000

ble = bluetooth.BLE()
ble.active(True)


class Beacon:

    name = b"uBeacon" + hexlify(ble.config("mac")[1][4:])

    def __str__(self):
        adv = self.adv_bytes
        return "bytes: {:d} data: {:s}".format(len(adv), hexlify(adv))

    @property
    def adv_bytes(self):
        return bytes(self.adv)

    @property
    def resp(self):
        return (
            [
                FLAGS_LENGHT,
                FLAGS_TYPE,
                FLAGS_DATA,
                len(self.name) + 1,
                _ADV_TYPE_NAME
            ]
            + [x for x in self.name]
        )

    @property
    def resp_bytes(self):
        return bytes(self.resp)

    def advertise(self):
        ble.gap_advertise(
            _ADV_INTERVAL_MS,
            adv_data=self.adv_bytes,
            resp_data=self.resp_bytes,
            connectable=False,
        )
