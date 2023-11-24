import unittest

from ubeacon import Beacon
from ubeacon.lintech import LinTechBeacon
from ubeacon.ibeacon import iBeacon
from ubeacon.mikrotik import MikroTik
from ubeacon.ruuvitag import RuuviTag
from ubeacon.altbeacon import AltBeacon
from ubeacon.eddystone import EddystoneUID, EddystoneURL


class ValidationTest(unittest.TestCase):

    beacon = Beacon()

    def test_validate_error(self):
        beacon = Beacon()
        self.assertEqual(beacon.validate(b"MicroPython BLE!", 16), b"MicroPython BLE!")
        self.assertEqual(
            beacon.validate(bytes([0, 0, 0, 0, 0, 1]), 6), b"\x00\x00\x00\x00\x00\x01"
        )
        self.assertEqual(beacon.validate(123, 1), b"{")

        self.assertRaises(ValueError, beacon.validate, b"MicroPython BLE!!!", 16)
        self.assertRaises(ValueError, beacon.validate, 1.1, 1)
        self.assertRaises(ValueError, beacon.validate, "1", 1)
        self.assertRaises(ValueError, beacon.validate, [1], 1)


class AltBeaconTest(unittest.TestCase):

    uuid = "3df93d5a-a1f2-47bb-a3cf-3e49e6a89bb6"

    company_id = 1337  # 2-bytes
    major = 17
    minor = 42
    reference_rssi = -69
    mfg_reserved = 35

    adv_data = b'\x02\x01\x06\x1b\xff9\x05\xbe\xac=\xf9=Z\xa1\xf2G\xbb\xa3\xcf>I\xe6\xa8\x9b\xb6\x00\x11\x00*\xbb#'

    def test_encode(self):
        beacon = AltBeacon(
            company_id=self.company_id,
            uuid=self.uuid,
            major=self.major,
            minor=self.minor,
            reference_rssi=self.reference_rssi,
            mfg_reserved=self.mfg_reserved,
        )
        self.assertEqual(beacon.adv_data, self.adv_data)

    def test_decode(self):
        beacon = AltBeacon(adv_data=self.adv_data)
        self.assertEqual(beacon.company_id, self.company_id)
        self.assertEqual(beacon.uuid, self.uuid)
        self.assertEqual(beacon.major, self.major)
        self.assertEqual(beacon.minor, self.minor)
        self.assertEqual(beacon.mfg_reserved, self.mfg_reserved)
        self.assertEqual(beacon.reference_rssi, self.reference_rssi)


class iBeaconTest(unittest.TestCase):

    uuid = "acbdf5ff-d272-45f5-8e45-01672fe51c47"
    major = 1337
    minor = 21
    reference_rssi = -65

    adv_data = b"\x02\x01\x06\x1a\xffL\x00\x02\x15\xac\xbd\xf5\xff\xd2rE\xf5\x8eE\x01g/\xe5\x1cG\x059\x00\x15\xbf"

    def test_encode(self):
        beacon = iBeacon(
            uuid=self.uuid,
            major=self.major,
            minor=self.minor,
            reference_rssi=self.reference_rssi,
        )
        self.assertEqual(beacon.adv_data, self.adv_data)

    def test_decode(self):
        beacon = iBeacon(adv_data=self.adv_data)
        self.assertEqual(beacon.uuid, self.uuid)
        self.assertEqual(beacon.major, self.major)
        self.assertEqual(beacon.minor, self.minor)
        self.assertEqual(beacon.reference_rssi, self.reference_rssi)


class LinTechBeaconTest(unittest.TestCase):
    uuid = "beff1020-2920-ff44-0103-ff4a400abfd7"  # 16-bytes
    major = 1025
    minor = 42
    reference_rssi = -69

    adv_data = b"\x02\x01\x06\x1b\xffD\x01\xff\x03\xbe\xff\x10 ) \xffD\x01\x03\xffJ@\n\xbf\xd7\x04\x01\x00*\xbb\xfc"

    def test_encode(self):
        beacon = LinTechBeacon(
            uuid=self.uuid,
            major=self.major,
            minor=self.minor,
            reference_rssi=self.reference_rssi,
        )
        self.assertEqual(beacon.adv_data, self.adv_data)

    def test_decode(self):
        beacon = LinTechBeacon(adv_data=self.adv_data)
        self.assertEqual(beacon.uuid, self.uuid)
        self.assertEqual(beacon.major, self.major)
        self.assertEqual(beacon.minor, self.minor)
        self.assertEqual(beacon.reference_rssi, self.reference_rssi)


class EddystoneUidTest(unittest.TestCase):

    namespace_id = "85b9ae954b59c3d6f69d"  # 10-bytes
    instance_id = "000000001337"  # 6-bytes
    reference_rssi = -65

    adv_data = b"\x03\x03\xaa\xfe\x17\x16\xaa\xfe\x00\xbf\x85\xb9\xae\x95KY\xc3\xd6\xf6\x9d\x00\x00\x00\x00\x137\x00\x00"

    def test_encode(self):
        beacon = EddystoneUID(
            namespace_id=self.namespace_id,
            instance_id=self.instance_id,
            reference_rssi=self.reference_rssi,
        )
        self.assertEqual(beacon.adv_data, self.adv_data)

    def test_decode(self):
        beacon = EddystoneUID(adv_data=self.adv_data)
        self.assertEqual(beacon.namespace_id, self.namespace_id)
        self.assertEqual(beacon.instance_id, self.instance_id)
        self.assertEqual(beacon.reference_rssi, self.reference_rssi)


class EddystoneUrlTest(unittest.TestCase):

    url = "https://micropython.com"
    reference_rssi = -68

    adv_data = b"\x03\x03\xaa\xfe\x12\x16\xaa\xfe\x10\xbc\x03micropython\x07"

    def test_encode(self):
        beacon = EddystoneURL(
            url=self.url,
            reference_rssi=self.reference_rssi,
        )
        self.assertEqual(beacon.adv_data, self.adv_data)

    def test_decode(self):
        beacon = EddystoneURL(adv_data=self.adv_data)
        self.assertEqual(beacon.url, self.url)
        self.assertEqual(beacon.reference_rssi, self.reference_rssi)

    def test_encode_url_unkonwn_tld(self):
        beacon = EddystoneURL(
            url="https://micropython.de",
            reference_rssi=self.reference_rssi,
        )
        self.assertEqual(
            beacon.adv_data,
            b"\x03\x03\xaa\xfe\x14\x16\xaa\xfe\x10\xbc\x03micropython.de",
        )


class RuuviTagTest(unittest.TestCase):

    adv_data_v5 = b"\x02\x01\x06\x1b\xff\x99\x04\x05\x12\xfcS\x94\xc3|\x00\x04\xff\xfc\x04\x0c\xac6B\x00\xcd\xcb\xb83L\x88O"

    def test_decode_df_5(self):
        beacon = RuuviTag(adv_data=self.adv_data_v5)
        self.assertEqual(beacon.data_format, 5)
        self.assertEqual(beacon.temperature, 24.3)
        self.assertEqual(beacon.humidity, 53.49)
        self.assertEqual(beacon.pressure, 100044)
        self.assertEqual(beacon.acceleration_x, 4)
        self.assertEqual(beacon.acceleration_y, -4)
        self.assertEqual(beacon.acceleration_z, 1036)
        self.assertEqual(beacon.battery_voltage, 2977)
        self.assertEqual(beacon.tx_power, 4)
        self.assertEqual(beacon.movement_counter, 66)
        self.assertEqual(beacon.measurement_sequence, 205)

    adv_data_v3 = b"\x03)\x1a\x1e\xce\x1e\xfc\x18\xf9B\x02\xca\x0bS"

    def test_decode_df_3(self):
        beacon = RuuviTag(adv_data=self.adv_data_v3)
        self.assertEqual(beacon.data_format, 3)
        self.assertEqual(beacon.temperature, 26.3)
        self.assertEqual(beacon.humidity, 20.5)
        self.assertEqual(beacon.pressure, 102766)
        self.assertEqual(beacon.acceleration_x, -1000)
        self.assertEqual(beacon.acceleration_y, -1726)
        self.assertEqual(beacon.acceleration_z, 714)
        self.assertEqual(beacon.battery_voltage, 2899)


class MikroTikBeaconTest(unittest.TestCase):

    adv_data = b"\x02\x01\x06\x15\xffO\t\x01\x00\xce\xa6\x00\x00\x00\x00\x02\x00\xa0\x1c\x91\x08W\x00\x00_"

    def test_decode(self):
        beacon = MikroTik(adv_data=self.adv_data)
        self.assertEqual(beacon.encrypted, 0)
        self.assertEqual(beacon.acceleration_x, 0)
        self.assertEqual(beacon.acceleration_y, 0)
        self.assertEqual(beacon.acceleration_z, 0.0078125)
        self.assertEqual(beacon.temperature, 28.625)
        self.assertEqual(beacon.uptime, 5703825)
        self.assertEqual(beacon.trigger, 0)
        self.assertEqual(beacon.battery, 95)


if __name__ == "__main__":
    unittest.main()
