"""
MikroTik Protocol Specification

https://help.mikrotik.com/docs/display/UM/MikroTik+Tag+advertisement+formats
"""

from struct import unpack

from . import Beacon


# Length of the data frame from the manufacturer specific ADV data structure.
# _ADV_LENGTH = const(0x15)

# Length of the payload data in the ADV data structure.
_DATA_LENGTH = const(0x12)


class MikroTik(Beacon):
    # The beacon device manufacturer's company identifier code.
    company_id = const(0x094F)

    def __init__(self, *, data=None):
        self.temperature = None

        # If adv_data is provided, decode it to initialize the beacon
        if data:
            self.decode(data)
        else:
            # If no adv_data, raise an error
            raise ValueError("Encoding is not supported)")

    def decode(self, data):
        """
        Decode the received advertising data and set the corresponding attributes
        """
        if len(data) != _DATA_LENGTH:
            raise ValueError("Invalid size")

        self.version = data[0]
        self.encrypted = bool(data[1])
        self.salt = unpack("<H", data[2:4])[0]
        self.acceleration_x = unpack("<H", data[4:6])[0] / 256
        self.acceleration_y = unpack("<H", data[6:8])[0] / 256
        self.acceleration_z = unpack("<H", data[8:10])[0] / 256

        temperature = unpack("<h", data[10:12])[0] / 256
        if temperature != -128.0:
            self.temperature = temperature

        self.uptime = unpack("<I", data[12:16])[0]
        self.trigger = data[16]
        self.battery = data[17]
