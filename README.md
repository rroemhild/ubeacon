# uBeacon

This library is in an early stage, things may change until there is a initial release.

## About

MicroPython library for encoding and decoding BLE beacons. This library does not handle the advertise or scan part, because of the different MicroPython forks handle bluetooth different ways.

Supported BLE Beacons

* AltBeacon
* Eddystone-UID
* Eddystone-URL
* iBeacon
* LinTech Beacon
* RuuviTag (decode only)


## Beacon Name

The beacon name is in the response data.

To be compatible with the MicroPython forks, uBeacon use `micropython.unique_id` to get an unique id based on the Wifi MAC address. To change the beacon name, it can be set after instatiation. For example use the last 2-Bytes from the Bluetooth MAC address:

```python
import bluetooth
from ubeacon.eddystone import EddystoneUID

ble = bluetooth.BLE()

beacon = EddystoneUID(NAMESPACE_ID, INSTANCE_ID)
beacon.name = b"uBeacon " + hexlify(ble.config("mac")[1][4:]).upper()
```


## Quickstart

Copy the ubeacon directory to your device. You can scip the beacon types you don't need for your project. `__init__.py` is mandatory. Find examples howto advertise the beacons in the examples directory.

### Encode

```python
from ubeacon.eddystone import EddystoneUID

NAMESPACE_ID = b"Eddystone!"  # 10-bytes
INSTANCE_ID = bytes([0, 0, 0, 0, 0, 1])  # 6-bytes

beacon = EddystoneUID(NAMESPACE_ID, INSTANCE_ID)
```

Type `beacon` to get the string representation of the uBeacon object:

```python
>>> beacon
EddystoneUID({'namespace_id': b'Eddystone!', 'instance_id': b'\x00\x00\x00\x00\x00\x01', 'reference_rssi': -70})
```

### Decode

```python
from ubeacon.altbeacon import AltBeacon

adv_data = b'\x02\x01\x06\x1b\xff\x18\x01\xbe\xacMicroPython BLE!\x15\x00\x00\x01\xba\x00'
beacon = AltBeacon(adv_data=adv_data)
```
