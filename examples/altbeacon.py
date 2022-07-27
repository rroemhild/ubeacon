import bluetooth
from ubeacon.altbeacon import AltBeacon


BEACON_ID_ORG_UNIT = b"MicroPython BLE!"  # 16-bytes
BEACON_ID_USE_CASE = bytes([21, 0, 0, 1])  # 4-bytes


def main():
    beacon = AltBeacon(BEACON_ID_ORG_UNIT, BEACON_ID_USE_CASE)
    beacon.advertise()


if __name__ == "__main__":
    main()
