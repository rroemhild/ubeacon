# ubeacon

__ubeacon__ is a MicroPython library designed for encoding and decoding BLE beacons. It does not handle the advertisement or scanning part directly, as different MicroPython forks handle Bluetooth in various ways.

Supported BLE beacons

* AltBeacon
* Eddystone-UID
* Eddystone-URL
* iBeacon
* LinTech Beacon
* RuuviTag (decode only)
* MikroTik (decode only)


## Beacon Naming

The beacon name is included in the response data.

To ensure compatibility with different MicroPython forks, __ubeacon__ utilizes `micropython.unique_id` to obtain a unique ID based on the Wi-Fi MAC address. To change the beacon name, it can be set after instantiation. For example, to use the last 2 bytes from the Bluetooth MAC address:

```python
import bluetooth
from ubeacon.eddystone import EddystoneUID

ble = bluetooth.BLE()

beacon = EddystoneUID(NAMESPACE, INSTANCE)
beacon.name = b"ubeacon " + hexlify(ble.config("mac")[1][4:]).upper()
```


## Quickstart

To get started, copy the *ubeacon* directory to your device. You may exclude the beacon types that are not required for your project, but please ensure to keep the *\_\_init\_\_.py* file as it is mandatory. You can find examples on how to advertise the beacons in the *examples* directory.

### Install with mip

```
mpremote mip install github:rroemhild/ubeacon
```

### Encode

```python
from ubeacon.eddystone import EddystoneUID

NAMESPACE = "85b9ae954b59c3d6f69d"  # 10-bytes
INSTANCE = "000000001337"  # 6-bytes

beacon = EddystoneUID(NAMESPACE, INSTANCE)
```

Type `beacon` into the REPL to get the string representation of the __ubeacon__ object:


```python
>>> beacon
EddystoneUID({"namespace": "85b9ae954b59c3d6f69d", "instance": "000000001337", "reference_rssi": -70})
```

### Decode

```python
from ubeacon.altbeacon import AltBeacon

adv_data = b"\x02\x01\x06\x1b\xff9\x05\xbe\xac=\xf9=Z\xa1\xf2G\xbb\xa3\xcf>I\xe6\xa8\x9b\xb6\x00\x11\x00*\xbb#"
beacon = AltBeacon(adv_data=adv_data)
```
