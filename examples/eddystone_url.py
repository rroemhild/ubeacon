import bluetooth
from ubeacon.eddystone import EddystoneURL, DOT_ORG


URL = b"micropython"

ADV_INTERVAL_MS = 250_000


def main():
    ble = bluetooth.BLE()
    ble.active(True)

    beacon = EddystoneURL(URL, url_tld=DOT_ORG)

    ble.gap_advertise(
        ADV_INTERVAL_MS,
        adv_data=beacon.adv_bytes,
        connectable=False,
    )


if __name__ == "__main__":
    main()
