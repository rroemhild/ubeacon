import bluetooth

from binascii import hexlify

from ubeacon import ADV_INTERVAL_MS
from ubeacon.eddystone import EddystoneUID


NAMESPACE_ID = b"eddystone!"  # 10-bytes
INSTANCE_ID = bytes([0, 0, 0, 0, 0, 1])  # 6-bytes


def main():
    ble = bluetooth.BLE()
    ble.active(True)

    beacon = EddystoneUID(NAMESPACE_ID, INSTANCE_ID)
    beacon.name = b"uBeacon " + hexlify(ble.config("mac")[1][4:]).upper()

    ble.gap_advertise(
        ADV_INTERVAL_MS,
        adv_data=beacon.adv_bytes,
        resp_data=beacon.resp_bytes,
        connectable=False,
    )


if __name__ == "__main__":
    main()
