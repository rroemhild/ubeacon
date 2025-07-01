"""
scan_async.py

Example script for asynchronously scanning Bluetooth Low Energy (BLE) beacons
using the aioble library with MicroPython. This script detects and identifies
various beacon types (Eddystone, iBeacon, AltBeacon, RuuviTag, MikroTik,
LinTech, SGWirelessCAPT) by parsing advertisement and manufacturer data.

Detected beacons are printed with their MAC address and parsed beacon data.
The scan runs asynchronously and can be stopped with a KeyboardInterrupt.

Dependencies:
  - aioble
  - asyncio
  - ubeacon.* beacon parsers

Usage:
  Run this script on a MicroPython device with BLE support.

Initialization:
  $ mpremote mip install aioble ubeacon
  $ mpremote cp examples/scan_async.py :main.py
"""

import aioble
import asyncio

from bluetooth import UUID

from ubeacon.ibeacon import IBeacon, IBEACON_COMPANY_ID
from ubeacon.lintech import LinTechBeacon, LINTECH_COMPANY_ID
from ubeacon.mikrotik import MikroTik, MIKROTIK_COMPANY_ID
from ubeacon.ruuvitag import RuuviTag, RUUVITAG_COMPANY_ID
from ubeacon.altbeacon import AltBeacon, ALTBEACON_DEVICE_TYPE
from ubeacon.eddystone import EddystoneUID, EddystoneURL, EDDYSTONE_UUID, EDDYSTONE_FRAME_TYPE_UID, EDDYSTONE_FRAME_TYPE_URL
from ubeacon.sgwireless import SGWirelessCAPT, SGWIRELESS_COMPANY_ID


_EDDYSTONE_UUID = UUID(0xFEAA)
_SCAN_DURATION_MS = const(0)


async def scan():
    async with aioble.scan(
        _SCAN_DURATION_MS, interval_us=30000, window_us=30000, active=False
    ) as scanner:
        async for result in scanner:
            beacon = False
            # Check for Eddystone beacons
            if _EDDYSTONE_UUID in result.services():
                frame_type = result.adv_data[8]
                if frame_type == EDDYSTONE_FRAME_TYPE_UID:
                    beacon = EddystoneUID(adv_data=result.adv_data)
                elif frame_type == EDDYSTONE_FRAME_TYPE_URL:
                    beacon = EddystoneURL(adv_data=result.adv_data)
            else:
                for mfg_id, mfg_data in result.manufacturer():
                    # LinTech
                    if mfg_id == LINTECH_COMPANY_ID:
                        beacon = LinTechBeacon(data=mfg_data)
                    # IBeacon
                    elif mfg_id == IBEACON_COMPANY_ID:
                        beacon = IBeacon(data=mfg_data)
                    # RuuviTag
                    elif mfg_id == RUUVITAG_COMPANY_ID:
                        beacon = RuuviTag(data=mfg_data)
                    # MikroTik
                    elif mfg_id == MIKROTIK_COMPANY_ID:
                        beacon = MikroTik(data=mfg_data)
                    # SGWirelessCAPT
                    elif mfg_id == SGWIRELESS_COMPANY_ID:
                        beacon = SGWirelessCAPT(data=mfg_data)
                    # AltBeacon
                    elif int.from_bytes(mfg_data[:2]) == ALTBEACON_DEVICE_TYPE:
                        beacon = AltBeacon(company_id=mfg_id, data=mfg_data)
            if beacon:
                print(f"MAC: {result.device.addr_hex()}, Beacon: {beacon,!r}")


if __name__ == "__main__":
    try:
        asyncio.run(scan())
    except KeyboardInterrupt:
        aioble.stop()
