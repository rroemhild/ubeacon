"""
Eddystone Protocol Specification: https://github.com/google/eddystone
"""

from binascii import hexlify
from micropython import const


_FLAGS_DATA = const(0x06)  # Discoverable, without BR/EDR support
_FLAGS_TYPE = const(0x01)
_FLAGS_LENGHT = const(0x02)

# A 1-byte value representing the average received signal strength at 0m from the advertiser
_REFERENCE_RSSI = const(0xD1)

_SERVICE_LENGTH = const(0x03)
_SERVICE_UUID_TYPES = const(0x03)

_EDDYSTONE_UUID = bytes([0xAA, 0xFE])
_EDDYSTONE_FRAME_LENGHT = const(0x17)
_EDDYSTONE_FRAME_TYPE_UID = const(0x00)
_EDDYSTONE_FRAME_TYPE_URL = const(0x10)
_EDDYSTONE_RESERVED = const(0x00)
_EDDYSTONE_SERVICE_DATA = const(0x16)

HTTP_WWW = const(0x00)
HTTPS_WWW = const(0x01)
HTTP = const(0x02)
HTTPS = const(0x03)
DOT_COM_SLASH = const(0x00)
DOT_ORG_SLASH = const(0x01)
DOT_EDU_SLASH = const(0x02)
DOT_NET_SLASH = const(0x03)
DOT_INFO_SLASH = const(0x04)
DOT_BIZ_SLASH = const(0x05)
DOT_GOV_SLASH = const(0x06)
DOT_COM = const(0x07)
DOT_ORG = const(0x08)
DOT_EDU = const(0x09)
DOT_NET = const(0x0A)
DOT_INFO = const(0x0B)
DOT_BIZ = const(0x0C)
DOT_GOV = const(0x0D)


class _Eddystone:
    def __str__(self):
        adv = self.adv_bytes
        return "bytes: {:d} data: {:s}".format(len(adv), hexlify(adv))

    @property
    def adv_bytes(self):
        return bytes(self.adv)


class EddystoneUID(_Eddystone):
    def __init__(
        self,
        namespace_id,  # 10-bytes
        instance_id,  # 6-bytes
        reference_rssi=_REFERENCE_RSSI,  # 1-byte
    ):
        self.namespace_id = namespace_id
        self.instance_id = instance_id
        self.reference_rssi = reference_rssi

    @property
    def adv(self):
        return (
            [
                _FLAGS_LENGHT,
                _FLAGS_TYPE,
                _FLAGS_DATA,
                _SERVICE_LENGTH,
                _SERVICE_UUID_TYPES,
            ]
            + [x for x in _EDDYSTONE_UUID]
            + [
                _EDDYSTONE_FRAME_LENGHT,
                _EDDYSTONE_SERVICE_DATA,
            ]
            + [x for x in _EDDYSTONE_UUID]
            + [
                _EDDYSTONE_FRAME_TYPE_UID,
                self.reference_rssi,
            ]
            + [x for x in self.namespace_id]
            + [x for x in self.instance_id]
            + [
                _EDDYSTONE_RESERVED,
                _EDDYSTONE_RESERVED,
            ]
        )


class EddystoneURL(_Eddystone):
    def __init__(
        self,
        url,
        url_prefix=HTTPS,
        url_tld=None,
        reference_rssi=_REFERENCE_RSSI,
    ):
        self.url = url
        self.url_prefix = url_prefix
        self.url_tld = url_tld
        self.reference_rssi = reference_rssi

    @property
    def adv(self):
        if self.url_tld:
            url_lenght = 6 + len(self.url) + 1
        else:
            url_lenght = 6 + len(self.url)

        adv = (
            [
                _FLAGS_LENGHT,
                _FLAGS_TYPE,
                _FLAGS_DATA,
                _SERVICE_LENGTH,
                _SERVICE_UUID_TYPES,
            ]
            + [x for x in _EDDYSTONE_UUID]
            + [
                url_lenght,
                _EDDYSTONE_SERVICE_DATA,
            ]
            + [x for x in _EDDYSTONE_UUID]
            + [
                _EDDYSTONE_FRAME_TYPE_URL,
                self.reference_rssi,
                self.url_prefix,
            ]
            + [x for x in self.url]
        )

        if self.url_tld is not None:
            adv.append(self.url_tld)

        return adv
