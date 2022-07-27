import bluetooth
from ubeacon.eddystone import EddystoneUID


NAMESPACE_ID = b"eddystone!"  # 10-bytes
INSTANCE_ID = bytes([0, 0, 0, 0, 0, 1])  # 6-bytes


def main():
    beacon = EddystoneUID(NAMESPACE_ID, INSTANCE_ID)
    beacon.advertise()


if __name__ == "__main__":
    main()
