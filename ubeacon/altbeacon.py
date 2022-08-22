"""
AltBeacon Protocol Specification: https://github.com/AltBeacon/spec
"""

from struct import pack, unpack
from binascii import hexlify
from micropython import const

from . import Beacon, FLAGS_LENGHT, FLAGS_TYPE, FLAGS_DATA


# Type representing the Manufacturer Specific advertising data structure.
_AD_TYPE = const(0xFF)

# Length of the type and data portion of the Manufacturer Specific advertising data structure.
_AD_LENGHT = const(0x1B)

# The AltBeacon advertisement code
_BEACON_CODE = bytes([0xBE, 0xAC])

# The beacon device manufacturer's company identifier code.
_MFG_ID = bytes([0x18, 0x01])

# Reserved for use by the manufacturer to implement special features
_MFG_RESERVED = const(0x00)

# A 1-byte value representing the average received signal strength at 1m from the advertiser
_REFERENCE_RSSI = const(0xBA)


class AltBeacon(Beacon):
    def __init__(
        self,
        beacon_id_ou=None,  # 16-bytes
        beacon_id_uc=None,  # 4-bytes
        mfg_id=_MFG_ID,  # 2-byte
        reference_rssi=_REFERENCE_RSSI,  # 1-byte
        mfg_reserved=_MFG_RESERVED,  # 1-byte
        *,
        adv_data=None,
    ):
        if adv_data:
            self.decode(adv_data)
        elif beacon_id_ou and beacon_id_uc:
            self.mfg_id = mfg_id
            self.beacon_id_ou = beacon_id_ou
            self.beacon_id_uc = beacon_id_uc
            self.mfg_reserved = mfg_reserved
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
            + [x for x in self.mfg_id]
            + [x for x in _BEACON_CODE]
            + [x for x in self.beacon_id_ou]
            + [x for x in self.beacon_id_uc]
            + [
                self.reference_rssi,
                self.mfg_reserved,
            ]
        )

    def decode(self, adv_data):
        self.beacon_id_ou = adv_data[6:22]
        self.beacon_id_uc = adv_data[22:26]
        self.mfg_id = adv_data[2:4]
        self.reference_rssi = unpack("!b", bytes([adv_data[26]]))[0]
        self.mfg_reserved = adv_data[27]
