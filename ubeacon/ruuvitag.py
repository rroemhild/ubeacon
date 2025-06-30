"""
RuuviTag Protocol Specification

https://docs.ruuvi.com/communication/bluetooth-advertisements
"""

from struct import unpack

from . import Beacon

# RuuviTag data formats
_DATA_FORMAT_3 = const(0x03)
_DATA_FORMAT_5 = const(0x05)

# Length of the payload data in the ADV data structure for format 3 and 5
_DATA_LENGTH_3 = const(0x0E)
_DATA_LENGTH_5 = const(0x18)


class RuuviTag(Beacon):
    # The beacon device manufacturer's company identifier code.
    company_id = const(0x0499)

    def __init__(self, *, data):
        # If adv_data is provided, decode it to initialize the beacon
        if data:
            self.decode(data)
        else:
            # If no adv_data, raise an error
            raise ValueError("Encoding is not supported)")

    def decode(self, data):
        data_format = data[0]
        if data_format == _DATA_FORMAT_3:
            self.decode_3(data)
        elif data_format == _DATA_FORMAT_5:
            self.decode_5(data)
        else:
            raise ValueError(f"Unsupported data format: {data_format}")

    def decode_3(self, data):
        """Decode data format 3 (RAWv1)"""
        if len(data) != _DATA_LENGTH_3:
            raise ValueError("Invalid payload data size")

        self.data_format = _DATA_FORMAT_3

        self.humidity = data[1] / 2

        temp = data[2] + data[3] / 100
        if temp > 128:
            temp -= 128
            temp = round(0 - temp, 2)
        self.temperature = temp

        self.pressure = unpack(">H", data[4:6])[0] + 50000

        self.acceleration_x = unpack(">h", data[6:8])[0]
        self.acceleration_y = unpack(">h", data[8:10])[0]
        self.acceleration_z = unpack(">h", data[10:12])[0]
        self.battery_voltage = unpack(">H", data[12:14])[0]

    def decode_5(self, data):
        """Decode data format 5 (RAWv2)"""
        if len(data) != _DATA_LENGTH_5:
            raise ValueError("Invalid payload data size")

        self.data_format = _DATA_FORMAT_5

        self.temperature = unpack(">h", data[1:3])[0] * 0.005
        self.humidity = unpack(">H", data[3:5])[0] * 0.0025
        self.pressure = unpack(">H", data[5:7])[0] + 50000

        self.acceleration_x = unpack(">h", data[7:9])[0]
        self.acceleration_y = unpack(">h", data[9:11])[0]
        self.acceleration_z = unpack(">h", data[11:13])[0]

        power = unpack(">H", data[13:15])[0]
        self.battery_voltage = (power >> 5) + 1600
        self.tx_power = (power & 0x1F) * 2 - 40

        self.movement_counter = data[15]
        self.measurement_sequence = unpack(">H", data[16:18])[0]
