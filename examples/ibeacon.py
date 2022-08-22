import bluetooth

from binascii import hexlify

from ubeacon import ADV_INTERVAL_MS
from ubeacon.ibeacon import iBeacon


UUID = bytes([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 23, 21, 42])  # 16-bytes
MAJOR = bytes([0, 1])  # 2-bytes
MINOR = bytes([0, 2])  # 2-bytes


def main():
    ble = bluetooth.BLE()
    ble.active(True)

    beacon = iBeacon(UUID, MAJOR, MINOR)
    beacon.name = b"uBeacon " + hexlify(ble.config("mac")[1][4:]).upper()

    ble.gap_advertise(
        ADV_INTERVAL_MS,
        adv_data=beacon.adv_bytes,
        resp_data=beacon.resp_bytes,
        connectable=False,
    )


if __name__ == "__main__":
    main()
