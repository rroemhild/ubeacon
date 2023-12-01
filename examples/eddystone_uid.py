import bluetooth

from ubeacon.eddystone import EddystoneUID


NAMESPACE = "85b9ae954b59c3d6f69d"
INSTANCE = "000000001337"

ADV_INTERVAL_MS = 250_000


def main():
    ble = bluetooth.BLE()
    ble.active(True)

    beacon = EddystoneUID(namespace=NAMESPACE, instance=INSTANCE)

    ble.gap_advertise(
        ADV_INTERVAL_MS,
        adv_data=beacon.adv_data,
        resp_data=beacon.resp_bytes,
        connectable=False,
    )


if __name__ == "__main__":
    main()
