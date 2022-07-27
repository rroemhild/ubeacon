import bluetooth
from ubeacon.ibeacon import iBeacon


UUID = bytes([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 23, 21, 42])  # 16-bytes
MAJOR = bytes([0, 1])  # 2-bytes
MINOR = bytes([0, 2])  # 2-bytes


def main():
    beacon = iBeacon(UUID, MAJOR, MINOR)
    beacon.advertise()


if __name__ == "__main__":
    main()
