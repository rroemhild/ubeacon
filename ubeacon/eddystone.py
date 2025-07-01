"""
Eddystone Protocol Specification

https://github.com/google/eddystone
"""

from struct import pack, unpack
from binascii import hexlify, unhexlify

from . import Beacon


# A 1-byte value representing the average received signal strength at 0m from the advertiser
_REFERENCE_RSSI = const(-70)

_SERVICE_LENGTH = const(0x03)
_SERVICE_UUID_TYPES = const(0x03)

EDDYSTONE_FRAME_TYPE_UID = const(0x00)
EDDYSTONE_FRAME_TYPE_URL = const(0x10)

_EDDYSTONE_COMPANY_ID = const(0xFEAA)
_EDDYSTONE_FRAME_LENGTH = const(0x17)
_EDDYSTONE_FRAME_LENGTH_LEGACY = const(0x15)
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
        adv = bytearray((
            _SERVICE_LENGTH,
            _SERVICE_UUID_TYPES,
        ))
        adv.extend(pack("<H", _EDDYSTONE_COMPANY_ID))
        adv.append(_EDDYSTONE_FRAME_LENGTH)
        adv.append(_EDDYSTONE_SERVICE_DATA)
        adv.extend(pack("<H", _EDDYSTONE_COMPANY_ID))
        adv.append(EDDYSTONE_FRAME_TYPE_UID)
        adv.extend(self.validate(pack(">b", self.reference_rssi), 1))
        adv.extend(self.validate(unhexlify(self.namespace), 10))
        adv.extend(self.validate(unhexlify(self.instance), 6))
        adv.append(_EDDYSTONE_RESERVED)
        adv.append(_EDDYSTONE_RESERVED)
        return adv

    def decode(self, adv_data):
        """
        Decode the received advertising data and set the corresponding attributes
        """
        adv_length = len(adv_data[5:])
        if (
            adv_length != _EDDYSTONE_FRAME_LENGTH
            and adv_length != _EDDYSTONE_FRAME_LENGTH_LEGACY
        ):
            raise ValueError("Invalid size of Eddystone UID frame")

        self.reference_rssi = unpack(">b", adv_data[9:10])[0]
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

        adv = bytearray([
            _SERVICE_LENGTH,
            _SERVICE_UUID_TYPES,
        ])
        adv.extend(pack("<H", _EDDYSTONE_COMPANY_ID))
        adv.append(url_frame_length)
        adv.append(_EDDYSTONE_SERVICE_DATA)
        adv.extend(pack("<H", _EDDYSTONE_COMPANY_ID))
        adv.append(EDDYSTONE_FRAME_TYPE_URL)
        adv.extend(self.validate(pack(">b", self.reference_rssi), 1))
        adv.append(url_scheme)
        adv.extend(url)
        return adv

    def decode(self, adv_data):
        """
        Decode the received advertising data and set the corresponding attributes
        """
        # Skip the first 4 bytes (service data header)
        adv_data = adv_data[4:]
        frame_length = adv_data[0]

        # Extract URL scheme and encoded URL
        scheme_idx = adv_data[6]
        url = bytearray(_URL_SCHEME[scheme_idx])
        url += adv_data[7 : frame_length + 1]

        # Replace TLD IDs with actual TLDs
        i = 0
        while i < len(url):
            byte = url[i]
            if 0 <= byte <= 13:
                tld = _URL_TLD[byte]
                url[i:i+1] = tld
                i += len(tld)
            else:
                i += 1

        self.url = url.decode()
        self.reference_rssi = unpack(">b", bytes([adv_data[5]]))[0]
