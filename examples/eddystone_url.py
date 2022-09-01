import bluetooth

from binascii import hexlify

from ubeacon.eddystone import EddystoneURL


URL = b"https://micropython.com"

ADV_INTERVAL_MS = 250_000


def main():
    ble = bluetooth.BLE()
    ble.active(True)

    beacon = EddystoneURL(URL)

    ble.gap_advertise(
        ADV_INTERVAL_MS,
        adv_data=beacon.adv_bytes,
        resp_data=beacon.resp_bytes,
        connectable=False,
    )


if __name__ == "__main__":
    main()
