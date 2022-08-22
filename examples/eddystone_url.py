import bluetooth

from binascii import hexlify

from ubeacon import ADV_INTERVAL_MS
from ubeacon.eddystone import EddystoneURL


URL = b"https://micropython.com"


def main():
    ble = bluetooth.BLE()
    ble.active(True)

    beacon = EddystoneURL(URL)
    beacon.name = b"uBeacon " + hexlify(ble.config("mac")[1][4:]).upper()

    ble.gap_advertise(
        ADV_INTERVAL_MS,
        adv_data=beacon.adv_bytes,
        resp_data=beacon.resp_bytes,
        connectable=False,
    )


if __name__ == "__main__":
    main()
