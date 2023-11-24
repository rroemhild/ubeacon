import ubinascii

from network import Bluetooth
from ubinascii import hexlify
from micropython import const

from ubeacon.lintech import LinTechBeacon
from ubeacon.ibeacon import iBeacon
from ubeacon.altbeacon import AltBeacon
from ubeacon.eddystone import EddystoneUID, EddystoneURL


_LINTECH = True
_IBEACON = True
_ALTBEACON = True
_EDDYSTONE = True


_LINTECH = bytes([0x44, 0x01])
_IBEACON = bytes([0x4C, 0x00])
_RUUVITAG = bytes([0x99, 0x04])
_ALTBEACON = bytes([0xBE, 0xAC])
_EDDYSTONE = bytes([0xAA, 0xFE])
_EDDYSTONE_UID = const(0x00)
_EDDYSTONE_URL = const(0x10)


def main():
    bluetooth = Bluetooth()
    bluetooth.start_scan(-1)

    while bluetooth.isscanning():
        beacon = None
        adv = bluetooth.get_adv()

        if adv:
            data = adv.data

            # Parse beacons
            if data[1] == 0xFF:
                if _ALTBEACON and data[4:6] == _ALTBEACON:
                    beacon = AltBeacon(adv_data=data)
                elif _IBEACON and data[2:4] == _IBEACON:
                    beacon = iBeacon(adv_data=data)
                elif _LINTECH and data[2:4] == _LINTECH:
                    beacon = LinTechBeacon(adv_data=data)
            elif _EDDYSTONE and data[2:4] == _EDDYSTONE:
                frame_type = data[8]

                if frame_type == _EDDYSTONE_UID:
                    beacon = EddystoneUID(adv_data=data)
                elif frame_type == _EDDYSTONE_URL:
                    beacon = EddystoneURL(adv_data=data)

            if beacon:
                print("{!r}".format(beacon))


if __name__ == "__main__":
    main()
