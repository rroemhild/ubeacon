import bluetooth

from binascii import hexlify

from ubeacon.altbeacon import AltBeacon


UUID = "3df93d5a-a1f2-47bb-a3cf-3e49e6a89bb6"
MAJOR = 17
MINOR = 42

ADV_INTERVAL_MS = 250_000


def main():
    ble = bluetooth.BLE()
    ble.active(True)

    beacon = AltBeacon(uuid=UUID, major=MAJOR, minor=MINOR)
    beacon.name = b"ubeacon " + hexlify(ble.config("mac")[1][4:]).upper()

    ble.gap_advertise(
        ADV_INTERVAL_MS,
        adv_data=beacon.adv_data,
        resp_data=beacon.resp_bytes,
        connectable=False,
    )


if __name__ == "__main__":
    main()
