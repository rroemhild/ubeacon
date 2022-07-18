"""
AltBeacon Protocol Specification: https://github.com/AltBeacon/spec
"""

from binascii import hexlify
from micropython import const


_FLAGS_DATA = const(0x06)  # Discoverable, without BR/EDR support
_FLAGS_TYPE = const(0x01)
_FLAGS_LENGHT = const(0x02)

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


class AltBeacon:
    def __init__(
        self,
        beacon_id_ou,  # 16-bytes
        beacon_id_uc,  # 4-bytes
        mfg_id=_MFG_ID,  # 1-byte
        reference_rssi=_REFERENCE_RSSI,  # 1-byte
        mfg_reserved=_MFG_RESERVED,  # 1-byte
    ):
        self.mfg_id = mfg_id
        self.beacon_id_ou = beacon_id_ou
        self.beacon_id_uc = beacon_id_uc
        self.mfg_reserved = mfg_reserved
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
            + [x for x in self.mfg_id]
            + [x for x in _BEACON_CODE]
            + [x for x in self.beacon_id_ou]
            + [x for x in self.beacon_id_uc]
            + [
                self.reference_rssi,
                self.mfg_reserved,
            ]
        )

    @property
    def adv_bytes(self):
        return bytes(self.adv)
