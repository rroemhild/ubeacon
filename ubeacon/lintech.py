"""
LinTech Beacon Protocol Specification: https://www.lintech.de/support/downloads/bluetooth-low-energy-smart-beacon/
"""

from struct import pack, unpack
from binascii import hexlify
from micropython import const

from . import Beacon, FLAGS_LENGHT, FLAGS_TYPE, FLAGS_DATA, ADV_TYPE_MFG_DATA


# The beacon device manufacturer's company identifier code.
_COMPANY_ID = bytes([0x44, 0x01])

# LinTech beacon advertisement code
_DEVICE_TYPE = bytes([0xFF, 0x03])

# Length of the data frame from the manufacturer specific ADV data structure.
_ADV_LENGHT = const(0x1B)

# A 1-byte value representing the average received signal strength at 1m from the advertiser
_REFERENCE_RSSI = const(0xC5)

# LinTech Beacon Proximity UUID
_PROXIMITY_UUID = bytes(
    [
        0xBE,
        0xFF,
        0x10,
        0x20,
        0x29,
        0x20,
        0xFF,
        0x44,
        0x01,
        0x03,
        0xFF,
        0x4A,
        0x40,
        0x0A,
        0xBF,
        0xD7,
    ]
)

# TX Power & Battery Level is, set to a fixed value for test only
_TX_BAT_STATUS = const(0xFC)


class LinTechBeacon(Beacon):
    def __init__(
        self,
        major=None,  # 2-bytes
        minor=None,  # 2-bytes
        reference_rssi=_REFERENCE_RSSI,  # 1-byte
        *,
        adv_data=None,
    ):
        if adv_data:
            self.decode(adv_data)
        elif major and minor:
            self.major = major
            self.minor = minor
            self.reference_rssi = reference_rssi
        else:
            raise ValueError("Could not initialize beacon")

    @property
    def adv(self):
        return (
            [
                FLAGS_LENGHT,
                FLAGS_TYPE,
                FLAGS_DATA,
                _ADV_LENGHT,
                ADV_TYPE_MFG_DATA,
            ]
            + [x for x in COMPANY_ID]
            + [x for x in DEVICE_TYPE]
            + [x for x in self.uuid]
            + [x for x in self.major]
            + [x for x in self.minor]
            + [
                self.reference_rssi,
                _TX_BAT_STATUS,
            ]
        )

    def decode(self, adv_data):
        self.major = unpack("!H", adv_data[22:24])[0]
        self.minor = unpack("!H", adv_data[24:26])[0]
        self.reference_rssi = unpack("!b", bytes([adv_data[26]]))[0]
        self.tx_power = adv_data[27] & 0b111
        self.battery_level = adv_data[27] >> 3
