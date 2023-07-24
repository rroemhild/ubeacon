"""
AltBeacon Protocol Specification: https://github.com/AltBeacon/spec
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
    ubeaconDecorators,
)


# Beacon device manufacturer's company identifier code.
# Default for AltBeacon is Radius Networks, Inc.
_COMPANY_ID = bytes([0x18, 0x01])

# AltBeacon advertisement code
_DEVICE_TYPE = bytes([0xBE, 0xAC])

# Length of the data frame from the manufacturer specific ADV data structure.
_ADV_LENGHT = const(0x1B)

# Reserved for use by the manufacturer to implement special features
_MFG_RESERVED = const(0x00)

# A 1-byte value representing the average received signal strength at 1m from the advertiser
_REFERENCE_RSSI = const(-70)


class AltBeacon(Beacon):
    def __init__(
        self,
        beacon_id_ou=None,  # 16-bytes
        beacon_id_uc=None,  # 4-bytes
        company_id=_COMPANY_ID,  # 2-byte
        reference_rssi=_REFERENCE_RSSI,  # 1-byte
        mfg_reserved=_MFG_RESERVED,  # 1-byte
        *,
        adv_data=None,
    ):
        # If adv_data is provided, decode it to initialize the beacon
        if adv_data:
            self.decode(adv_data)
        # If beacon_id_ou and beacon_id_uc are provided, use them to initialize the beacon
        elif beacon_id_ou and beacon_id_uc:
            self.company_id = company_id
            self.beacon_id_ou = beacon_id_ou
            self.beacon_id_uc = beacon_id_uc
            self.mfg_reserved = mfg_reserved
            self.reference_rssi = reference_rssi
        else:
            # If neither adv_data nor required IDs are provided, raise an error
            raise ValueError("Could not initialize beacon")

    @property
    def adv(self):
        """Generate the advertising data for the AltBeacon"""
        return (
            [
                FLAGS_LENGHT,
                FLAGS_TYPE,
                FLAGS_DATA,
                _ADV_LENGHT,
                ADV_TYPE_MFG_DATA,
            ]
            + [x for x in self.validate(self.company_id, 2)]
            + [x for x in _DEVICE_TYPE]
            + [x for x in self.validate(self.beacon_id_ou, 16)]
            + [x for x in self.validate(self.beacon_id_uc, 4)]
            + [
                self.validate(self.reference_rssi, 1)[0],
                self.validate(self.mfg_reserved, 1)[0],
            ]
        )

    @ubeaconDecorators.remove_adv_header
    def decode(self, adv_data):
        """
        Decode the received advertising data and set the corresponding attributes
        """
        self.beacon_id_ou = adv_data[6:22]
        self.beacon_id_uc = adv_data[22:26]
        self.company_id = adv_data[2:4]
        self.reference_rssi = unpack("!b", bytes([adv_data[26]]))[0]
        self.mfg_reserved = adv_data[27]
