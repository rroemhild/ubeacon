"""
RuuviTag Protocol Specification: https://docs.ruuvi.com/communication/bluetooth-advertisements
"""

from struct import unpack

from . import Beacon, ubeaconDecorators


_DATA_FORMAT_3 = const(0x03)
_DATA_FORMAT_5 = const(0x05)
_RUUVITAG_ADV = b"\x99\x04"


class RuuviTag(Beacon):
    def __init__(self, *, adv_data):
        self.decode(adv_data)

    @ubeaconDecorators.remove_adv_header
    def decode(self, adv_data):
        # Strip advertisement data
        if _RUUVITAG_ADV in adv_data[:4]:
            adv_data = adv_data[4:]

        data_format = adv_data[0]  # RuuviTag data format

        if data_format == _DATA_FORMAT_3:
            self.decode_data_format_3(adv_data)
        elif data_format == _DATA_FORMAT_5:
            self.decode_data_format_5(adv_data)

    def decode_data_format_3(self, adv_data):
        """Data format 3 (RAWv1)"""
        self.data_format = _DATA_FORMAT_3

        self.humidity = adv_data[1] / 2

        temperature = adv_data[2] + adv_data[3] / 100
        if temperature > 128:
            temperature -= 128
            temperature = round(0 - temperature, 2)
        self.temperature = temperature

        self.pressure = unpack(">H", adv_data[4:6])[0] + 50000

        self.acceleration_x = unpack(">h", adv_data[6:8])[0]
        self.acceleration_y = unpack(">h", adv_data[8:10])[0]
        self.acceleration_z = unpack(">h", adv_data[10:12])[0]
        self.battery_voltage = unpack(">H", adv_data[12:14])[0]

    def decode_data_format_5(self, adv_data):
        """Data format 5 (RAWv2)"""
        self.data_format = _DATA_FORMAT_5

        self.temperature = unpack(">h", adv_data[1:3])[0] * 0.005
        self.humidity = unpack(">H", adv_data[3:5])[0] * 0.0025
        self.pressure = unpack(">H", adv_data[5:7])[0] + 50000

        self.acceleration_x = unpack(">h", adv_data[7:9])[0]
        self.acceleration_y = unpack(">h", adv_data[9:11])[0]
        self.acceleration_z = unpack(">h", adv_data[11:13])[0]

        power_bin = bin(unpack(">H", adv_data[13:15])[0])[2:]
        self.battery_voltage = int(power_bin[:11], 2) + 1600
        self.tx_power = int(power_bin[11:], 2) * 2 - 40

        self.movement_counter = adv_data[15]
        self.measurement_sequence = unpack(">H", adv_data[16:18])[0]
