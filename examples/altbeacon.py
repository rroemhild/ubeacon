import bluetooth

from binascii import hexlify

from ubeacon.altbeacon import AltBeacon


BEACON_ID_ORG_UNIT = b"MicroPython BLE!"  # 16-bytes
BEACON_ID_USE_CASE = bytes([21, 0, 0, 1])  # 4-bytes

ADV_INTERVAL_MS = 250_000


def main():
    ble = bluetooth.BLE()
    ble.active(True)

    beacon = AltBeacon(BEACON_ID_ORG_UNIT, BEACON_ID_USE_CASE)
    beacon.name = b"uBeacon " + hexlify(ble.config("mac")[1][4:]).upper()

    ble.gap_advertise(
        ADV_INTERVAL_MS,
        adv_data=beacon.adv_bytes,
        resp_data=beacon.resp_bytes,
        connectable=False,
    )


if __name__ == "__main__":
    main()
