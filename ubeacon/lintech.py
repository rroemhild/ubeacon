"""
LinTech Beacon Protocol Specification: https://www.lintech.de/support/downloads/bluetooth-low-energy-smart-beacon/
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


# The beacon device manufacturer's company identifier code.
_COMPANY_ID = const(0x0144)  # bytes([0x44, 0x01])

# LinTech beacon advertisement code
_DEVICE_TYPE = const(0xFF03)  # bytes([0xFF, 0x03])

# Length of the data frame from the manufacturer specific ADV data structure.
_ADV_LENGTH = const(0x1B)

# Value representing the average received signal strength at 1m from the advertiser
_REFERENCE_RSSI = const(-70)

# LinTech Beacon Proximity UUID
_PROXIMITY_UUID = "beff1020-2920-ff44-0103-ff4a400abfd7"

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
        # If adv_data is provided, decode it to initialize the beacon
        if adv_data:
            self.decode(adv_data)
        # If major and minor are provided, use them to initialize the beacon
        elif major and minor:
            self.uuid = uuid
            self.major = major
            self.minor = minor
            self.reference_rssi = reference_rssi
        else:
            # If neither adv_data nor required values are provided, raise an error
            raise ValueError("Could not initialize beacon")

    @property
    def adv(self):
        """Generate the advertising data for the LinTech beacon"""
        return (
            [
                FLAGS_LENGTH,
                FLAGS_TYPE,
                FLAGS_DATA,
                _ADV_LENGTH,
                ADV_TYPE_MFG_DATA,
            ]
            + [x for x in pack("<H", _COMPANY_ID)]
            + [x for x in pack(">H", _DEVICE_TYPE)]
            + [x for x in self.validate(self.uuid_to_bin(self.uuid), 16)]
            + [x for x in self.validate(pack(">H", self.major), 2)]
            + [x for x in self.validate(pack(">H", self.minor), 2)]
            + [
                self.validate(pack(">b", self.reference_rssi), 1)[0],
                _TX_BAT_STATUS,
            ]
        )

    @ubeaconDecorators.remove_adv_header
    def decode(self, adv_data):
        """
        Decode the received advertising data and set the corresponding attributes
        """
        if len(adv_data[1:]) != _ADV_LENGTH:
            raise ValueError("Invalid size")

        self.uuid = str(UUID(adv_data[6:22]))
        self.major = unpack(">H", adv_data[22:24])[0]
        self.minor = unpack(">H", adv_data[24:26])[0]
        self.reference_rssi = unpack(">b", bytes([adv_data[26]]))[0]
        self.tx_power = adv_data[27] & 0b111
        self.battery_level = adv_data[27] >> 3
