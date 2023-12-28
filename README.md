# uBeacon

__uBeacon__ is a simple Bluetooth Low Energy (BLE) beacon library for MicroPython. It can be used to create beacons for BLE advertisement or to decode advertised beacons. It does not handle the advertisement or scanning part directly, as different MicroPython forks handle Bluetooth in various ways.

Supported BLE beacons:

* AltBeacon
* Eddystone-UID
* Eddystone-URL
* iBeacon
* LinTech Beacon
* RuuviTag (decode only)
* MikroTik (decode only)


## Installation

### Install with mip

You can install __uBeacon__ with mip using the following command:

```
mpremote mip install github:rroemhild/ubeacon
```

### Copy files

You can also manually copy the files from the `ubeacon` directory to your MicroPython device. You may exclude the beacon types that are not required for your project, ensure to keep the *\_\_init\_\_.py* file as it is mandatory.

```sh
mpremote mkdir lib/ubeacon
mpremote cp ubeacon/* :lib/ubeacon
```

## Usage

The __uBeacon__ library provides several examples in the `examples` directory, where you can find examples on how to advertise a beacon and decode beacons scanned by your device.

### Advertise Beacon

To advertise a beacon, you first need to create a beacon object using one of the provided classes. For example, to create an iBeacon object:

```python
from ubeacon.ibeacon import IBeacon

beacon = IBeacon(
    uuid="acbdf5ff-d272-45f5-8e45-01672fe51c47",
    major=42,
    minor=21,
)
```

Once you have created a beacon object, you can start advertising it using i.e. the `bluetooth.BLE` module:

```python
import bluetooth

ble = bluetooth.BLE()
ble.active(True)
ble.gap_advertise(250_000, adv_data=beacon.adv_data, resp_data=beacon.resp_bytes, connectable=False)
```

### Decode Beacon

To decode a beacon, you first need to obtain the beacon data from a scan result. The data is typically stored in a format like `adv_data`. For example:

```python
from ubeacon.altbeacon import AltBeacon

adv_data = b"\x02\x01\x06\x1b\xff9\x05\xbe\xac=\xf9=Z\xa1\xf2G\xbb\xa3\xcf>I\xe6\xa8\x9b\xb6\x00\x11\x00*\xbb#"
beacon = AltBeacon(adv_data=adv_data)
print(f"{beacon,!r}")
```

### Filter Beacon

The __uBeacon__ library provides a `BeaconFilter` class that allows you to filter beacons based on their UUID, Major, and Minor. For example:

```python
from ubeacon import BeaconFilter

# Initialize the filter object to filter by uuid and major
beacon_filter = BeaconFilter(
    uuid="7dc04cb6-ed25-420a-ae02-f31674a1f946",
    major=1337,
)

if not beacon_filter.match(beacon):
    print("Beacon does not match filter.")
```

## Beacon Naming

The beacon name is included in the response data.

To ensure compatibility with different MicroPython forks, __uBeacon__ utilizes `micropython.unique_id` to obtain a unique ID based on the Wi-Fi MAC address. To change the beacon name, it can be set after instantiation. For example, to use the last 2 bytes from the Bluetooth MAC address:

```python
import bluetooth
from ubeacon.eddystone import EddystoneUID

NAMESPACE = "85b9ae954b59c3d6f69d"
INSTANCE = "000000001337"

ble = bluetooth.BLE()

beacon = EddystoneUID(NAMESPACE, INSTANCE)
beacon.name = b"ubeacon " + hexlify(ble.config("mac")[1][4:]).upper()
```
