"""
RuuviTag Protocol Specification

https://docs.ruuvi.com/communication/bluetooth-advertisements
"""

from struct import unpack

from . import Beacon


# The beacon device manufacturer's company identifier code.
RUUVITAG_COMPANY_ID = const(0x0499)

# RuuviTag data formats
_DATA_FORMAT_3 = const(0x03)
_DATA_FORMAT_5 = const(0x05)

# Length of the payload data in the ADV data structure for format 3 and 5
_DATA_LENGTH_3 = const(0x0E)
_DATA_LENGTH_5 = const(0x18)


class RuuviTag(Beacon):
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

        (
            hum_raw,
            temp_int,
            temp_frac,
            pres_raw,
            acc_x,
            acc_y,
            acc_z,
            bat_v
        ) = unpack(">BBBHhhhH", data[1:14])

        self.humidity = hum_raw / 2

        t = temp_int + temp_frac / 100
        if t > 128:
            t -= 128
            t = round(0 - t, 2)
        self.temperature = t

        self.pressure = pres_raw + 50000

        self.acceleration_x = acc_x
        self.acceleration_y = acc_y
        self.acceleration_z = acc_z
        self.battery_voltage = bat_v

    def decode_5(self, data):
        """Decode data format 5 (RAWv2)"""
        if len(data) != _DATA_LENGTH_5:
            raise ValueError("Invalid payload data size")

        self.data_format = _DATA_FORMAT_5

        (
            temp_raw,
            hum_raw,
            pres_raw,
            acc_x,
            acc_y,
            acc_z,
            power,
            mov,
            seq
        ) = unpack(">hHHhhhHBH", data[1:18])

        self.temperature = temp_raw * 0.005
        self.humidity = hum_raw * 0.0025
        self.pressure = pres_raw + 50000

        self.acceleration_x = acc_x
        self.acceleration_y = acc_y
        self.acceleration_z = acc_z

        self.battery_voltage = (power >> 5) + 1600
        self.tx_power = (power & 0x1F) * 2 - 40

        self.movement_counter = mov
        self.measurement_sequence = seq
