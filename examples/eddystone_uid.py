import bluetooth

from binascii import hexlify

from ubeacon.eddystone import EddystoneUID


NAMESPACE_ID = "85b9ae954b59c3d6f69d"  # 10-bytes
INSTANCE_ID = "000000001337"  # 6-bytes

ADV_INTERVAL_MS = 250_000


def main():
    ble = bluetooth.BLE()
    ble.active(True)

    beacon = EddystoneUID(NAMESPACE_ID, INSTANCE_ID)

    ble.gap_advertise(
        ADV_INTERVAL_MS,
        adv_data=beacon.adv_data,
        resp_data=beacon.resp_bytes,
        connectable=False,
    )


if __name__ == "__main__":
    main()
