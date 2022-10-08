"""
LinTech Beacon Protocol Specification: https://www.lintech.de/support/downloads/bluetooth-low-energy-smart-beacon/
"""

from struct import pack, unpack
from binascii import hexlify
from micropython import const

from . import (
    Beacon,
    FLAGS_LENGHT,
    FLAGS_TYPE,
    FLAGS_DATA,
    ADV_TYPE_MFG_DATA,
    uBeaconDecorators,
)


# The beacon device manufacturer's company identifier code.
_COMPANY_ID = bytes([0x44, 0x01])

# LinTech beacon advertisement code
_DEVICE_TYPE = bytes([0xFF, 0x03])

# Length of the data frame from the manufacturer specific ADV data structure.
_ADV_LENGHT = const(0x1B)

# Value representing the average received signal strength at 1m from the advertiser
_REFERENCE_RSSI = const(-70)

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
        uuid=_PROXIMITY_UUID,  # 16-bytes
        major=None,  # 0 - 65535
        minor=None,  # 0 - 65535
        reference_rssi=_REFERENCE_RSSI,  # 1-byte
        *,
        adv_data=None,
    ):
        if adv_data:
            self.decode(adv_data)
        elif major and minor:
            self.uuid = uuid
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
            + [x for x in _COMPANY_ID]
            + [x for x in _DEVICE_TYPE]
            + [x for x in self.validate(self.uuid, 16)]
            + [x for x in self.validate(self.major, 2)]
            + [x for x in self.validate(self.minor, 2)]
            + [
                self.validate(self.reference_rssi, 1)[0],
                _TX_BAT_STATUS,
            ]
        )

    @uBeaconDecorators.remove_adv_header
    def decode(self, adv_data):
        self.uuid = adv_data[6:22]
        self.major = unpack("!H", adv_data[22:24])[0]
        self.minor = unpack("!H", adv_data[24:26])[0]
        self.reference_rssi = unpack("!b", bytes([adv_data[26]]))[0]
        self.tx_power = adv_data[27] & 0b111
        self.battery_level = adv_data[27] >> 3
