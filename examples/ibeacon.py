import bluetooth

from ubeacon.ibeacon import IBeacon


UUID = "acbdf5ff-d272-45f5-8e45-01672fe51c47"
MAJOR = 42
MINOR = 21

ADV_INTERVAL_MS = 250_000


def main():
    ble = bluetooth.BLE()
    ble.active(True)

    beacon = IBeacon(uuid=UUID, major=MAJOR, minor=MINOR)

    ble.gap_advertise(
        ADV_INTERVAL_MS,
        adv_data=beacon.adv_data,
        resp_data=beacon.resp_bytes,
        connectable=False,
    )


if __name__ == "__main__":
    main()
