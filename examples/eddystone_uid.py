import bluetooth

from binascii import hexlify

from ubeacon.eddystone import EddystoneUID


NAMESPACE_ID = b"Eddystone!"  # 10-bytes
INSTANCE_ID = bytes([0, 0, 0, 0, 0, 1])  # 6-bytes

ADV_INTERVAL_MS = 250_000


def main():
    ble = bluetooth.BLE()
    ble.active(True)

    beacon = EddystoneUID(NAMESPACE_ID, INSTANCE_ID)

    ble.gap_advertise(
        ADV_INTERVAL_MS,
        adv_data=beacon.adv_bytes,
        resp_data=beacon.resp_bytes,
        connectable=False,
    )


if __name__ == "__main__":
    main()
