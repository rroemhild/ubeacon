"""
iBeacon Protocol Specification: https://developer.apple.com/ibeacon/
"""

from struct import pack, unpack
from binascii import hexlify
from micropython import const

from . import Beacon, FLAGS_LENGHT, FLAGS_TYPE, FLAGS_DATA


# Type representing the Manufacturer Specific advertising data structure.
_AD_TYPE = const(0xFF)

# Length of the type and data portion of the Manufacturer Specific advertising data structure.
_AD_LENGHT = const(0x1A)

_BEACON_TYPE = bytes([0x02, 0x15])

# The beacon device manufacturer's company identifier code.
_MFG_ID = bytes([0x4C, 0x00])

# A 1-byte value representing the average received signal strength at 1m from the advertiser
_REFERENCE_RSSI = const(0xBA)


class iBeacon(Beacon):
    def __init__(
        self,
        uuid=None,  # 16-bytes
        major=None,  # 2-bytes
        minor=None,  # 2-bytes
        reference_rssi=_REFERENCE_RSSI,
        *,
        adv_data=None
    ):
        if adv_data:
            self.decode(adv_data)
        elif uuid and major and minor:
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
                _AD_LENGHT,
                _AD_TYPE,
            ]
            + [x for x in _MFG_ID]
            + [x for x in _BEACON_TYPE]
            + [x for x in self.uuid]
            + [x for x in self.major]
            + [x for x in self.minor]
            + [
                self.reference_rssi,
                0x00,
            ]
        )

    def decode(self, adv_data):
        self.uuid = adv_data[6:22]
        self.major = adv_data[22:24]
        self.minor = adv_data[24:26]
        self.reference_rssi = unpack("!b", bytes([adv_data[26]]))[0]
