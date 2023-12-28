"""
Eddystone Protocol Specification: https://github.com/google/eddystone
"""

from struct import pack, unpack
from binascii import hexlify, unhexlify

from . import Beacon


# A 1-byte value representing the average received signal strength at 0m from the advertiser
_REFERENCE_RSSI = const(-70)

_SERVICE_LENGTH = const(0x03)
_SERVICE_UUID_TYPES = const(0x03)

_EDDYSTONE_UUID = const(0xFEAA)
_EDDYSTONE_FRAME_LENGTH = const(0x17)
_EDDYSTONE_FRAME_LENGTH_LEGACY = const(0x15)
_EDDYSTONE_FRAME_TYPE_UID = const(0x00)
_EDDYSTONE_FRAME_TYPE_URL = const(0x10)
_EDDYSTONE_RESERVED = const(0x00)
_EDDYSTONE_SERVICE_DATA = const(0x16)

_URL_SCHEME = (
    b"http://www.",
    b"https://www.",
    b"http://",
    b"https://",
)

_URL_TLD = (
    b".com/",
    b".org/",
    b".edu/",
    b".net/",
    b".info/",
    b".biz/",
    b".gov/",
    b".com",
    b".org",
    b".edu",
    b".net",
    b".info",
    b".biz",
    b".gov",
)


class EddystoneUID(Beacon):
    def __init__(
        self,
        namespace=None,  # 10-bytes
        instance=None,  # 6-bytes
        reference_rssi=_REFERENCE_RSSI,  # 1-byte
        *,
        adv_data=None,
    ):
        # If adv_data is provided, decode it to initialize the beacon
        if adv_data:
            self.decode(adv_data)
        # If namespace_id and instance_id are provided, use them to initialize the beacon
        elif namespace and instance:
            self.namespace = namespace
            self.instance = instance
            self.reference_rssi = reference_rssi
        else:
            # If neither adv_data nor required IDs are provided, raise an error
            raise ValueError("Could not initialize beacon")

    @property
    def adv(self):
        """Generate the advertising data for the EddystoneUID beacon"""
        return (
            [
                _SERVICE_LENGTH,
                _SERVICE_UUID_TYPES,
            ]
            + [x for x in pack("<H", _EDDYSTONE_UUID)]
            + [
                _EDDYSTONE_FRAME_LENGTH,
                _EDDYSTONE_SERVICE_DATA,
            ]
            + [x for x in pack("<H", _EDDYSTONE_UUID)]
            + [
                _EDDYSTONE_FRAME_TYPE_UID,
                self.validate(pack(">b", self.reference_rssi), 1)[0],
            ]
            + [x for x in self.validate(unhexlify(self.namespace), 10)]
            + [x for x in self.validate(unhexlify(self.instance), 6)]
            + [
                _EDDYSTONE_RESERVED,
                _EDDYSTONE_RESERVED,
            ]
        )

    def decode(self, adv_data):
        """
        Decode the received advertising data and set the corresponding attributes
        """
        adv_length = len(adv_data[5:])
        if (
            adv_length != _EDDYSTONE_FRAME_LENGTH
            and adv_length != _EDDYSTONE_FRAME_LENGTH_LEGACY
        ):
            raise ValueError("Invalid size.")

        self.reference_rssi = unpack(">b", bytes([adv_data[9]]))[0]
        self.namespace = hexlify(adv_data[10:20]).decode()
        self.instance = hexlify(adv_data[20:26]).decode()


class EddystoneURL(Beacon):
    def __init__(self, url=None, reference_rssi=_REFERENCE_RSSI, *, adv_data=None):
        # If adv_data is provided, decode it to initialize the beacon
        if adv_data:
            self.decode(adv_data)
        # If url is provided, use it to initialize the beacon
        elif url:
            self.url = url.encode()
            self.reference_rssi = reference_rssi
        else:
            raise ValueError("Could not initialize beacon")

    @property
    def adv(self):
        """Generate the advertising data for the EddystoneURL beacon"""
        url = self.url
        url_scheme = 3

        # Set URL scheme and remove scheme from url
        for key, val in enumerate(_URL_SCHEME):
            if url.startswith(val):
                url = url.replace(val, b"")
                url_scheme = key

        # Find and replace top level domain
        for key, val in enumerate(_URL_TLD):
            if val in url:
                url = url.replace(val, bytes([key]))

        # Length is URL length plus first 6 bytes from Eddystone URL frame
        url_frame_length = len(url) + 6

        return (
            [
                _SERVICE_LENGTH,
                _SERVICE_UUID_TYPES,
            ]
            + [x for x in pack("<H", _EDDYSTONE_UUID)]
            + [
                url_frame_length,
                _EDDYSTONE_SERVICE_DATA,
            ]
            + [x for x in pack("<H", _EDDYSTONE_UUID)]
            + [
                _EDDYSTONE_FRAME_TYPE_URL,
                self.validate(self.reference_rssi, 1)[0],
                url_scheme,
            ]
            + [x for x in url]
        )

    def decode(self, adv_data):
        """
        Decode the received advertising data and set the corresponding attributes
        """
        url = b""

        # Only Eddystone URL frame
        adv_data = adv_data[4:]
        frame_length = adv_data[0]

        # Join the URL together
        url += _URL_SCHEME[adv_data[6]]
        url += adv_data[7 : frame_length + 1]

        # Replace TLD ID if any
        for byte in url:
            if byte <= 13:
                url = url.replace(bytes([byte]), _URL_TLD[byte])

        self.url = url.decode()
        self.reference_rssi = unpack(">b", bytes([adv_data[5]]))[0]
