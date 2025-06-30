"""
SG Wireless CAP/T Protocol Specification

https://docs.sgwireless.com/wp-content/uploads/2024/11/SGW8130D-CAP-T-Datasheet_v1.0-Nov-2024.pdf
"""

from struct import unpack

from . import Beacon


# Length of the data frame from the manufacturer specific ADV data structure.
# _ADV_LENGTH = const(0x0b)

# Length of the payload data in the ADV data structure.
_DATA_LENGTH = const(0x08)


class SGWirelessCAPT(Beacon):
    # The beacon device manufacturer's company identifier code.
    company_id = const(0x0059)

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
        if len(data) == 7:
            pass # Unsuported Type 2 frame with firmware version
        elif len(data) != _DATA_LENGTH:
            raise ValueError(f"Invalid payload data size")
        else:
            self.temperature = unpack("<h", data[0:2])[0] / 100
            self.humidity = unpack("<H", data[2:4])[0] / 100
            self.battery = data[4]
