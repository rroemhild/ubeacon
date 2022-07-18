"""
iBeacon Protocol Specification: https://developer.apple.com/ibeacon/
"""

from binascii import hexlify
from micropython import const


_FLAGS_DATA = const(0x06)  # Discoverable, without BR/EDR support
_FLAGS_TYPE = const(0x01)
_FLAGS_LENGHT = const(0x02)

# Type representing the Manufacturer Specific advertising data structure.
_AD_TYPE = const(0xFF)

# Length of the type and data portion of the Manufacturer Specific advertising data structure.
_AD_LENGHT = const(0x1A)

_BEACON_TYPE = bytes([0x02, 0x15])

# The beacon device manufacturer's company identifier code.
_MFG_ID = bytes([0x4C, 0x00])

# A 1-byte value representing the average received signal strength at 1m from the advertiser
_REFERENCE_RSSI = const(0xBA)


class iBeacon:
    def __init__(
        self,
        uuid,  # 16-bytes
        major,  # 2-bytes
        minor,  # 2-bytes
        reference_rssi=_REFERENCE_RSSI,
    ):
        self.uuid = uuid
        self.major = major
        self.minor = minor
        self.reference_rssi = reference_rssi

    def __str__(self):
        adv = self.adv_bytes
        return "bytes: {:d} data: {:s}".format(len(adv), hexlify(adv))

    @property
    def adv(self):
        return (
            [
                _FLAGS_LENGHT,
                _FLAGS_TYPE,
                _FLAGS_DATA,
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

    @property
    def adv_bytes(self):
        return bytes(self.adv)
