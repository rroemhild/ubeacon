import bluetooth

from binascii import hexlify

from ubeacon.ibeacon import iBeacon


UUID = bytes([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 23, 21, 42])  # 16-bytes
MAJOR = 42  # 0 - 65535
MINOR = 21  # 0 - 65535

ADV_INTERVAL_MS = 250_000


def main():
    ble = bluetooth.BLE()
    ble.active(True)

    beacon = iBeacon(UUID, MAJOR, MINOR)

    ble.gap_advertise(
        ADV_INTERVAL_MS,
        adv_data=beacon.adv_bytes,
        resp_data=beacon.resp_bytes,
        connectable=False,
    )


if __name__ == "__main__":
    main()
