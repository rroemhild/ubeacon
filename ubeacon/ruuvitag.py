"""
RuuviTag Protocol Specification: hhttps://docs.ruuvi.com/communication/bluetooth-advertisements
"""

from struct import unpack
from micropython import const

from . import Beacon, uBeaconDecorators


_DATA_FORMAT_3 = const(0x03)
_DATA_FORMAT_5 = const(0x05)


class RuuviTag(Beacon):
    def __init__(self, *, adv_data):
        self.decode(adv_data)

    @property
    def adv(self):
        raise NotImplementedError("ADV Data is not supported")

    @uBeaconDecorators.remove_adv_header
    def decode(self, adv_data):
        data_format = adv_data[4]

        if data_format == _DATA_FORMAT_3:
            self.data_format = 3
            self.decode_data_format_3(adv_data)
        elif data_format == _DATA_FORMAT_5:
            self.data_format = 5
            self.decode_data_format_5(adv_data)

    def decode_data_format_3(self, adv_data):
        """Data format 3 (RAWv1)"""
        self.humidity = adv_data[5] / 2

        temperature = adv_data[6] + adv_data[7] / 100
        if temperature > 128:
            temperature -= 128
            temperature = round(0 - temperature, 2)
        self.temperature = temperature

        self.pressure = unpack("!H", adv_data[8:10])[0] + 50000

        self.acceleration_x = unpack("!h", adv_data[10:12])[0]
        self.acceleration_y = unpack("!h", adv_data[12:14])[0]
        self.acceleration_z = unpack("!h", adv_data[14:16])[0]
        self.battery_voltage = unpack("!H", adv_data[16:18])[0]

    def decode_data_format_5(self, adv_data):
        """Data format 5 (RAWv2)"""
        self.temperature = unpack("!h", adv_data[5:7])[0] * 0.005
        self.humidity = unpack("!H", adv_data[7:9])[0] * 0.0025
        self.pressure = unpack("!H", adv_data[9:11])[0] + 50000

        self.acceleration_x = unpack("!h", adv_data[11:13])[0]
        self.acceleration_y = unpack("!h", adv_data[13:15])[0]
        self.acceleration_z = unpack("!h", adv_data[15:17])[0]

        power_bin = bin(unpack("!H", adv_data[17:19])[0])[2:]
        self.battery_voltage = int(power_bin[:11], 2) + 1600
        self.tx_power = int(power_bin[11:], 2) * 2 - 40

        self.movement_counter = adv_data[20]
        self.measurement_sequence = unpack("!H", adv_data[20:22])[0]
