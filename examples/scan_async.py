import aioble
import uasyncio as asyncio
import bluetooth

from ubinascii import hexlify

from ubeacon import uBeaconDecorators
from ubeacon.lintech import LinTechBeacon
from ubeacon.ibeacon import iBeacon
from ubeacon.ruuvitag import RuuviTag
from ubeacon.altbeacon import AltBeacon
from ubeacon.eddystone import EddystoneUID, EddystoneURL


# Beacon advertisement codes
_LINTECH_UUID = bluetooth.UUID(0x0144)
_IBEACON_UUID = bluetooth.UUID(0x004C)
_RUUVITAG_UUID = bluetooth.UUID(0x0499)
_ALTBEACON_UUID = bluetooth.UUID(0x0118)
_ALTBEACON_DEVICE_TYPE = bytes([0xBE, 0xAC])
_EDDYSTONE_UUID = bluetooth.UUID(0xFEAA)
_EDDYSTONE_UID = const(0x00)
_EDDYSTONE_URL = const(0x10)


_SCAN_DURATION_MS = 10000


async def scan():
    print("start scan")

    async with aioble.scan(
        _SCAN_DURATION_MS, interval_us=16000, window_us=16000
    ) as scanner:
        async for result in scanner:
            beacon = None

            if result.adv_data:
                if _EDDYSTONE_UUID in result.services():
                    frame_type = result.adv_data[8]

                    if frame_type == _EDDYSTONE_UID:
                        beacon = EddystoneUID(adv_data=result.adv_data)
                    elif frame_type == _EDDYSTONE_URL:
                        beacon = EddystoneURL(adv_data=result.adv_data)
                else:
                    for mfg_id, mfg_data in result.manufacturer():
                        uuid = bluetooth.UUID(mfg_id)

                        if uuid == _LINTECH_UUID:
                            beacon = LinTechBeacon(adv_data=result.adv_data)
                        elif uuid == _IBEACON_UUID:
                            beacon = iBeacon(adv_data=result.adv_data)
                        elif uuid == _RUUVITAG_UUID:
                            beacon = RuuviTag(adv_data=result.adv_data)
                        elif (
                            uuid == _ALTBEACON_UUID
                            or mfg_data[:2] == _ALTBEACON_DEVICE_TYPE
                        ):
                            beacon = AltBeacon(adv_data=result.adv_data)

            if beacon:
                print("MAC: {} Type: {!r}".format(hexlify(result.device.addr), beacon))


if __name__ == "__main__":
    asyncio.run(scan())
