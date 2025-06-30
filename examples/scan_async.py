import aioble
import asyncio
import bluetooth

from ubeacon.lintech import LinTechBeacon
from ubeacon.ibeacon import IBeacon
from ubeacon.ruuvitag import RuuviTag
from ubeacon.altbeacon import AltBeacon
from ubeacon.eddystone import EddystoneUID, EddystoneURL
from ubeacon.mikrotik import MikroTik
# from ubeacon.sgwireless import SGWirelessCAPT


# Beacon advertisement codes
_ALTBEACON_DEVICE_TYPE = bytes([0xBE, 0xAC])
_EDDYSTONE_UUID = bluetooth.UUID(0xFEAA)
_EDDYSTONE_UID = const(0x00)
_EDDYSTONE_URL = const(0x10)

_SCAN_DURATION_MS = const(0)


async def scan():
    async with aioble.scan(
        _SCAN_DURATION_MS, interval_us=30000, window_us=30000, active=False
    ) as scanner:
        async for result in scanner:
            beacon = False

            if _EDDYSTONE_UUID in result.services():
                frame_type = result.adv_data[8]
                print(f"Eddystone adv data: {result.adv_data}")
                if frame_type == _EDDYSTONE_UID:
                    beacon = EddystoneUID(adv_data=result.adv_data)
                elif frame_type == _EDDYSTONE_URL:
                    beacon = EddystoneURL(adv_data=result.adv_data)
            else:
                for mfg_id, mfg_data in result.manufacturer():
                    if mfg_id == LinTechBeacon.company_id:
                        beacon = LinTechBeacon(data=mfg_data)
                    # elif mfg_id == IBeacon.company_id:
                    #     beacon = IBeacon(data=mfg_data)
                    # elif mfg_id == RuuviTag.company_id:
                    #     beacon = RuuviTag(data=mfg_data)
                    # elif mfg_id == MikroTik.company_id:
                    #     beacon = MikroTik(adv_data=result.adv_data)
                    elif mfg_data[:2] == _ALTBEACON_DEVICE_TYPE:
                        beacon = AltBeacon(company_id=mfg_id, data=mfg_data)
            if beacon:
                print(f"MAC: {result.device.addr_hex()}, Beacon: {beacon,!r}")


if __name__ == "__main__":
    try:
        asyncio.run(scan())
    except KeyboardInterrupt:
        aioble.stop()
