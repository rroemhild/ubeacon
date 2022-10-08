import sys

from binascii import hexlify
from micropython import const


FLAGS_DATA = const(0x06)  # Discoverable, without BR/EDR support
FLAGS_TYPE = const(0x01)
FLAGS_LENGHT = const(0x02)

# ADV data frame  type for the manufacturer specific ADV data structure
ADV_TYPE_MFG_DATA = const(0xFF)

# ADV data frame Frame type for complete local name
_ADV_TYPE_COMPLETE_NAME = const(0x09)


def _unique_id():
    if sys.platform == "linux":
        return b"LINUX"
    elif sys.platform == "esp32":
        import bluetooth

        ble = bluetooth.BLE()
        ble.active(True)
        id = ble.config("mac")[1][4:]
        ble.active(False)
        return hexlify(id).upper()
    elif sys.platform.endswith("Py"):  # PyCom
        import machine

        return hexlify(machine.unique_id()[4:]).upper()


class uBeaconDecorators:
    @classmethod
    def remove_adv_header(cls, decorated):
        """Decorator to remove the ADV data flags header if any"""

        def inner(cls, adv_data):
            if adv_data[:2] == bytes([0x02, 0x01]):
                adv_data = adv_data[3:]
            decorated(cls, adv_data)

        return inner


class Beacon:

    # Use the Wifi MAC address to get a 2-byte unique id
    name = b"uBeacon " + _unique_id()

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
            _ADV_TYPE_COMPLETE_NAME,
        ] + [x for x in self.name]

    @property
    def resp_bytes(self):
        return bytes(self.resp)

    def decode(self, adv_data):
        raise NotImplementedError("No decode method in child class implemented")

    @staticmethod
    def validate(value, size: int) -> bytes:
        value_bytes = b""

        if isinstance(value, bytes):
            value_bytes = value
            if len(value_bytes) != size:
                raise ValueError("Value has to be {}-bytes long".format(size))
        elif isinstance(value, int):
            value_bytes = value.to_bytes(size, "big")
        else:
            raise ValueError("Value has to be int or bytes")

        return value_bytes
