"""
AltBeacon Protocol Specification: https://github.com/AltBeacon/spec
"""

from struct import pack, unpack

from . import (
    UUID,
    Beacon,
    FLAGS_LENGTH,
    FLAGS_TYPE,
    FLAGS_DATA,
    ADV_TYPE_MFG_DATA,
    ubeaconDecorators,
)


# Beacon device manufacturer's company identifier code.
# Default for AltBeacon is Radius Networks, Inc.
_COMPANY_ID = const(0x0118)

# AltBeacon advertisement code
_DEVICE_TYPE = const(0xBEAC)

# Length of the data frame from the manufacturer specific ADV data structure.
_ADV_LENGTH = const(0x1B)

# Reserved for use by the manufacturer to implement special features
_MFG_RESERVED = const(0x01)

# A 1-byte value representing the average received signal strength at 1m from the advertiser
_REFERENCE_RSSI = const(-70)


class AltBeacon(Beacon):
    def __init__(
        self,
        company_id=_COMPANY_ID,  # 0 - 255
        uuid=None,  # c9ae8912-0c99-471d-ac77-d013f4956c33
        major=None,  # 0 - 65535
        minor=None,  # 0 - 65535
        reference_rssi=_REFERENCE_RSSI,  # average received signal strength at 1m
        mfg_reserved=_MFG_RESERVED,  # 1-byte
        *,
        adv_data=None,
    ):
        # If adv_data is provided, decode it to initialize the beacon
        if adv_data:
            self.decode(adv_data)
        # If uuid, major and minor are provided, use them to initialize the beacon
        elif uuid and major and minor:
            self.company_id = company_id
            self.uuid = uuid
            self.major = major
            self.minor = minor
            self.reference_rssi = reference_rssi
            self.mfg_reserved = mfg_reserved
        else:
            # If neither adv_data nor required IDs are provided, raise an error
            raise ValueError("Could not initialize beacon")

    @property
    def adv(self):
        """Generate the advertising data for the AltBeacon"""
        return (
            [
                FLAGS_LENGTH,
                FLAGS_TYPE,
                FLAGS_DATA,
                _ADV_LENGTH,
                ADV_TYPE_MFG_DATA,
            ]
            + [x for x in self.validate(pack("<H", self.company_id), 2)]
            + [x for x in pack(">H", _DEVICE_TYPE)]
            + [x for x in self.validate(self.uuid_to_bin(self.uuid), 16)]
            + [x for x in self.validate(pack(">H", self.major), 2)]
            + [x for x in self.validate(pack(">H", self.minor), 2)]
            + [
                self.validate(pack(">b", self.reference_rssi), 1)[0],
                self.validate(self.mfg_reserved, 1)[0],
            ]
        )

    @ubeaconDecorators.remove_adv_header
    def decode(self, adv_data):
        """
        Decode the received advertising data and set the corresponding attributes
        """
        if len(adv_data[1:]) != _ADV_LENGTH:
            raise ValueError("Invalid size")

        self.company_id = unpack("<H", adv_data[2:4])[0]
        self.uuid = str(UUID(adv_data[6:22]))
        self.major = unpack(">H", adv_data[22:24])[0]
        self.minor = unpack(">H", adv_data[24:26])[0]
        self.reference_rssi = unpack(">b", bytes([adv_data[26]]))[0]
        self.mfg_reserved = adv_data[27]
