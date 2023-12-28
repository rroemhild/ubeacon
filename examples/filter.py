import aioble
import uasyncio as asyncio

from ubinascii import hexlify

from ubeacon import BeaconFilter
from ubeacon.ibeacon import IBeacon


_IBEACON_UUID = const(0x004C)
_SCAN_DURATION_MS = const(0)


async def scan():

    # Initialize the filter object to filter by uuid and major
    beacon_filter = BeaconFilter(
        uuid="7dc04cb6-ed25-420a-ae02-f31674a1f946",
        major=1337,
    )

    async with aioble.scan(_SCAN_DURATION_MS) as scanner:
        async for result in scanner:
            for mfg_id, _ in result.manufacturer():
                if mfg_id == _IBEACON_UUID:
                    beacon = IBeacon(adv_data=result.adv_data)

                    # Proceed if the beacon match the filter
                    if beacon_filter.match(beacon):
                        print(f"MAC: {hexlify(result.device.addr)} Beacon: {beacon,!r}")


if __name__ == "__main__":
    try:
        asyncio.run(scan())
    except KeyboardInterrupt:
        aioble.stop()
