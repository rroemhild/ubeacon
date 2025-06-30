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
            raise ValueError("Invalid payload data size")

        # Unpack all fields at once for efficiency
        (
            version,
            encrypted,
            salt,
            acc_x,
            acc_y,
            acc_z,
            temp_raw,
            uptime,
            trigger,
            bat
        ) = unpack("<BBHHHHhIBB", data)

        self.version = version
        self.encrypted = bool(encrypted)
        self.salt = salt
        self.acceleration_x = acc_x / 256
        self.acceleration_y = acc_y / 256
        self.acceleration_z = acc_z / 256

        t = temp_raw / 256
        if t != -128.0:
            self.temperature = t

        self.uptime = uptime
        self.trigger = trigger
        self.battery = bat
