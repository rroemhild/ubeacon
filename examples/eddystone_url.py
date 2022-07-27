import bluetooth
from ubeacon.eddystone import EddystoneURL, DOT_ORG


URL = b"micropython"


def main():
    beacon = EddystoneURL(URL, url_tld=DOT_ORG)
    beacon.advertise()


if __name__ == "__main__":
    main()
