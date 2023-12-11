"""
MikroTik Protocol Specification

https://help.mikrotik.com/docs/display/UM/MikroTik+Tag+advertisement+formats
"""

from struct import unpack

from . import Beacon, ubeaconDecorators


# Length of the data frame from the manufacturer specific ADV data structure.
_ADV_LENGTH = const(0x15)


class MikroTik(Beacon):
    def __init__(self, *, adv_data=None):
        self.temperature = None

        # If adv_data is provided, decode it to initialize the beacon
        if adv_data:
            self.decode(adv_data)
        else:
            # If no adv_data, raise an error
            raise ValueError("Could not initialize beacon")

    @ubeaconDecorators.remove_adv_header
    def decode(self, adv_data):
        """
        Decode the received advertising data and set the corresponding attributes
        """
        if len(adv_data[1:]) != _ADV_LENGTH:
            raise ValueError("Invalid size")

        self.version = adv_data[4]
        self.encrypted = bool(adv_data[5])
        self.salt = unpack("<H", adv_data[6:8])[0]
        self.acceleration_x = unpack("<H", adv_data[8:10])[0] / 256
        self.acceleration_y = unpack("<H", adv_data[10:12])[0] / 256
        self.acceleration_z = unpack("<H", adv_data[12:14])[0] / 256

        temperature = unpack("<h", adv_data[14:16])[0] / 256
        if temperature != -128.0:
            self.temperature = temperature

        self.uptime = unpack("<I", adv_data[16:20])[0]
        self.trigger = adv_data[20]
        self.battery = adv_data[21]
