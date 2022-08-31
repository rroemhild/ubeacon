"""
iBeacon Protocol Specification: https://developer.apple.com/ibeacon/
"""

from struct import unpack
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
_COMPANY_ID = bytes([0x4C, 0x00])

# iBeacon advertisement code
_DEVICE_TYPE = bytes([0x02, 0x15])

# Length of the data frame from the manufacturer specific ADV data structure.
_ADV_LENGHT = const(0x1A)

# Value representing the average received signal strength at 1m from the advertiser
_REFERENCE_RSSI = const(-70)


class iBeacon(Beacon):
    def __init__(
        self,
        uuid=None,  # 16-bytes
        major=None,  # 0 - 65535
        minor=None,  # 0 - 65535
        reference_rssi=_REFERENCE_RSSI,  # 1-byte
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
            ]
        )

    @uBeaconDecorators.remove_adv_header
    def decode(self, adv_data):
        self.uuid = adv_data[6:22]
        self.major = unpack("!H", adv_data[22:24])[0]
        self.minor = unpack("!H", adv_data[24:26])[0]
        self.reference_rssi = unpack("!b", bytes([adv_data[26]]))[0]
