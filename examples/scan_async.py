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
import bluetooth

from ubeacon.ibeacon import IBeacon
from ubeacon.lintech import LinTechBeacon
from ubeacon.mikrotik import MikroTik
from ubeacon.ruuvitag import RuuviTag
from ubeacon.altbeacon import AltBeacon
from ubeacon.eddystone import EddystoneUID, EddystoneURL
from ubeacon.sgwireless import SGWirelessCAPT

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
                if frame_type == _EDDYSTONE_UID:
                    beacon = EddystoneUID(adv_data=result.adv_data)
                elif frame_type == _EDDYSTONE_URL:
                    beacon = EddystoneURL(adv_data=result.adv_data)
            else:
                for mfg_id, mfg_data in result.manufacturer():
                    # LinTech
                    if mfg_id == LinTechBeacon.company_id:
                        beacon = LinTechBeacon(data=mfg_data)
                    # IBeacon
                    elif mfg_id == IBeacon.company_id:
                        beacon = IBeacon(data=mfg_data)
                    # RuuviTag
                    elif mfg_id == RuuviTag.company_id:
                        beacon = RuuviTag(data=mfg_data)
                    # MikroTik
                    elif mfg_id == MikroTik.company_id:
                        beacon = MikroTik(data=mfg_data)
                    # SGWirelessCAPT
                    elif mfg_id == SGWirelessCAPT.company_id:
                        beacon = SGWirelessCAPT(data=mfg_data)
                    # AltBeacon
                    elif mfg_data[:2] == _ALTBEACON_DEVICE_TYPE:
                        beacon = AltBeacon(company_id=mfg_id, data=mfg_data)
            if beacon:
                print(f"MAC: {result.device.addr_hex()}, Beacon: {beacon,!r}")


if __name__ == "__main__":
    try:
        asyncio.run(scan())
    except KeyboardInterrupt:
        aioble.stop()
