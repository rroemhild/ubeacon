"""
iBeacon Protocol Specification

https://developer.apple.com/ibeacon/
"""

from struct import pack, unpack

from . import (
    UUID,
    Beacon,
    FLAGS_LENGTH,
    FLAGS_TYPE,
    FLAGS_DATA,
    ADV_TYPE_MFG_DATA,
)

# The beacon device manufacturer's company identifier code.
IBEACON_COMPANY_ID = const(0x004C)

# iBeacon advertisement code
_DEVICE_TYPE = const(0x0215)

# Length of the data frame from the manufacturer specific ADV data structure.
_ADV_LENGTH = const(0x1A)

# Length of the payload data in the ADV data structure.
_DATA_LENGTH = const(0x17)

# Value representing the average received signal strength at 1m from the advertiser
_REFERENCE_RSSI = const(-70)


class IBeacon(Beacon):
    def __init__(
        self,
        uuid=None,  # c9ae8912-0c99-471d-ac77-d013f4956c33
        major=None,  # 0 - 65535
        minor=None,  # 0 - 65535
        reference_rssi=_REFERENCE_RSSI,  # 1-byte
        *,
        data=None
    ):
        # If adv_data is provided, decode it to initialize the beacon
        if data:
            self.decode(data)
        # If uuid, major and minor are provided, use them to initialize the beacon
        elif uuid and major and minor:
            self.uuid = uuid
            self.major = major
            self.minor = minor
            self.reference_rssi = reference_rssi
        else:
            # If neither payload data nor required values are provided, raise an error
            raise ValueError("Could not initialize beacon")

    @property
    def adv(self):
        """Generate the advertising data for the iBeacon"""
        adv = bytearray((
            FLAGS_LENGTH,
            FLAGS_TYPE,
            FLAGS_DATA,
            _ADV_LENGTH,
            ADV_TYPE_MFG_DATA,
        ))
        adv.extend(pack("<H", IBEACON_COMPANY_ID))
        adv.extend(pack(">H", _DEVICE_TYPE))
        adv.extend(self.validate(self.uuid_to_bin(self.uuid), 16))
        adv.extend(self.validate(pack(">H", self.major), 2))
        adv.extend(self.validate(pack(">H", self.minor), 2))
        adv.extend(self.validate(pack(">b", self.reference_rssi), 1))
        return adv

    def decode(self, data):
        """
        Decode the received advertising data and set the corresponding attributes
        """
        if len(data) != _DATA_LENGTH:
            raise ValueError("Invalid payload data size")

        self.uuid = str(UUID(data[2:18]))
        self.major, self.minor, self.reference_rssi = unpack(">HHb", data[18:23])
