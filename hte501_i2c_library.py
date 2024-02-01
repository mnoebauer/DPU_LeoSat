# -*- coding: utf-8 -*-
"""
Read functions for measurement values of the HTE501 Sensor via I2c interface.

Copyright 2023 E+E Elektronik Ges.m.b.H.

Disclaimer:
This application example is non-binding and does not claim to be complete with
regard to configuration and equipment as well as all eventualities. The
application example is intended to provide assistance with the HTE501 sensor
module design-in and is provided "as is".You yourself are responsible for the
proper operation of the products described. This application example does not
release you from the obligation to handle the product safely during
application, installation, operation and maintenance. By using this application
example, you acknowledge that we cannot be held liable for any damage beyond
the liability regulations described.

We reserve the right to make changes to this application example at any time
without notice. In case of discrepancies between the suggestions in this
application example and other E+E publications, such as catalogues, the content
of the other documentation takes precedence. We assume no liability for
the information contained in this document.
"""


# pylint: disable=E0401
from smbus2 import SMBus, i2c_msg
# pylint: enable=E0401
CRC8_ONEWIRE_POLY = 0x31
CRC8_ONEWIRE_START = 0xFF
HTE501_COMMAND_READ_SINGLE_SHOT = 0x2C1B
HTE501_COMMAND_READ_PERIODIC_MEASUREMENT = 0xE000
HTE501_COMMAND_READ_DEW_POINT = 0xE016
HTE501_COMMAND_READ_WRITE_SENSOR_SETTINGS = 0x72A7
HTE501_COMMAND_CLEAR_REGISTER_1 = 0x3041
HTE501_COMMAND_READ_REGISTER_1 = 0xF32D
HTE501_COMMAND_READ_REGISTER_2 = 0xF352
HTE501_COMMAND_START_PERIODIC_MEASUREMENT = 0x201E
HTE501_COMMAND_END_PERIODIC_MEASUREMENT = 0x3093
HTE501_COMMAND_SOFT_RESET = 0x30A2
HTE501_COMMAND_HEATER_ON = 0x306D
HTE501_COMMAND_HEATER_OFF = 0x3066
HTE501_COMMAND_READ_IDENTIFICATION = 0x7029
HTE501_REGISTER_PERIODIC_MEASUREMENT_TIME = 0x10
HTE501_REGISTER_HEATER_CURRENT = 0x08
HTE501_REGISTER_MEASUREMENT_RESOLUTION = 0x0F


def get_status_string(status_code):
    """Return string from status_code."""
    status_string = {
        0: "Success",
        1: "Not acknowledge error",
        2: "Checksum error",
        3: "Measurement error",
        4: "error wrong input for change_periodic_measurement_time",
        5: "error wrong input for change_heater_current",
        6: "error wrong input for change_measurement_resolution",
    }

    if status_code < len(status_string):
        return status_string[status_code]
    return "Unknown error"


def calc_crc8(buf, start, end):
    ''' calculate crc8 checksum  '''
    crc_val = CRC8_ONEWIRE_START
    for j in range(start, end):
        cur_val = buf[j]
        for _ in range(8):
            if ((crc_val ^ cur_val) & 0x80) != 0:
                crc_val = (crc_val << 1) ^ CRC8_ONEWIRE_POLY
            else:
                crc_val = crc_val << 1
            cur_val = cur_val << 1
    crc_val &= 0xFF
    return crc_val


class HTE501():
    """Implements communication with HTE501 over i2c with a specific address."""

    def __init__(self, i2c_address):
        self.i2c_address = i2c_address

    def get_single_shot_temp_hum(self):
        """Let the sensor take a measurement and return the temperature and humidity values."""
        i2c_response = self.wire_write_read(
            [(HTE501_COMMAND_READ_SINGLE_SHOT >> 8),
             (HTE501_COMMAND_READ_SINGLE_SHOT & 0xFF)], 6)
        if (i2c_response[2] == calc_crc8(i2c_response, 0, 2)) & (i2c_response[5] 
                                                                 == calc_crc8(i2c_response, 3, 5)):
            temperature = ((float)(i2c_response[0]) * 256 + i2c_response[1])
            if temperature > 55536:
                temperature = (temperature - 65536) / 100
            else:
                temperature = temperature / 100
            humidity = ((float)(i2c_response[3]) * 256 + i2c_response[4]) / 100
            return temperature, humidity
        else:
            raise Warning(get_status_string(2))

    def get_periodic_measurement_temp_hum(self):
        """Get the last measurement from the periodic measurement for temperature and humidity"""
        i2c_response = self.wire_write_read(
            [(HTE501_COMMAND_READ_PERIODIC_MEASUREMENT >> 8),
             (HTE501_COMMAND_READ_PERIODIC_MEASUREMENT & 0xFF)], 6)
        if (i2c_response[2] == calc_crc8(i2c_response, 0, 2)) & (i2c_response[5] ==
                                                                 calc_crc8(i2c_response, 3, 5)):
            temperature = ((float)(i2c_response[0]) * 256 + i2c_response[1])
            if temperature > 55536:
                temperature = (temperature - 65536) / 100
            else:
                temperature = temperature / 100
            humidity = ((float)(i2c_response[3]) * 256 + i2c_response[4]) / 100
            return temperature, humidity
        else:
            raise Warning(get_status_string(2))

    def get_dewpoint(self):
        """Get the calculated dewpoint from the last measurement"""
        i2c_response = self.wire_write_read(
            [(HTE501_COMMAND_READ_DEW_POINT >> 8),
             (HTE501_COMMAND_READ_DEW_POINT & 0xFF)], 3)
        if i2c_response[2] == calc_crc8(i2c_response, 0, 2):
            dewpoint = ((float)(i2c_response[0]) * 256 + i2c_response[1])
            if dewpoint > 55536:
                dewpoint = (dewpoint - 65536)/100
            else:
                dewpoint = dewpoint / 100
            return dewpoint
        else:
            raise Warning(get_status_string(2))

    def change_periodic_measurement_time(self, milli_sec):
        """chnage the time between measuremnts in the periodic measurement mode"""
        if milli_sec < 3276751:
            value = milli_sec/50
            send_bytes = [0, 0]
            send_bytes[1] = int(value / 255)
            send_bytes[0] = int(value % 256)
            self.wire_write(
                [(HTE501_COMMAND_READ_WRITE_SENSOR_SETTINGS >> 8),
                 (HTE501_COMMAND_READ_WRITE_SENSOR_SETTINGS & 0xFF),
                 HTE501_REGISTER_PERIODIC_MEASUREMENT_TIME,
                 send_bytes[0], send_bytes[1],
                 calc_crc8([0x10, send_bytes[0], send_bytes[1]], 0, 3)])
        else:
            raise Warning(get_status_string(4))

    def read_periodic_measurement_time(self):
        """reads the time between measuremnts in the periodic measurement mode"""
        i2c_response = self.wire_write_read(
            [(HTE501_COMMAND_READ_WRITE_SENSOR_SETTINGS >> 8),
             (HTE501_COMMAND_READ_WRITE_SENSOR_SETTINGS & 0xFF),
             HTE501_REGISTER_PERIODIC_MEASUREMENT_TIME], 2)
        value = i2c_response[1] * 256 + i2c_response[0]
        return value * 0.05

    def change_heater_current(self, current):
        """chnage the current that heats the sensor from 5 to 80 mA"""
        send_byte = 0x00
        if 5 <= current <= 80:
            value = int((current / 5) - 1)
            send_byte = value
            send_byte = ((send_byte << 3) + 7) & 255  # +7 because of Heater off
            self.wire_write(
                [(HTE501_COMMAND_READ_WRITE_SENSOR_SETTINGS >> 8),
                 (HTE501_COMMAND_READ_WRITE_SENSOR_SETTINGS & 0xFF),
                 HTE501_REGISTER_HEATER_CURRENT, send_byte,
                 calc_crc8([0x08, send_byte], 0, 2)])
        else:
            raise Warning(get_status_string(5))

    def read_heater_current(self):
        """read the current that heats the sensor"""
        i2c_response = self.wire_write_read(
            [(HTE501_COMMAND_READ_WRITE_SENSOR_SETTINGS >> 8),
             (HTE501_COMMAND_READ_WRITE_SENSOR_SETTINGS & 0xFF),
             HTE501_REGISTER_HEATER_CURRENT], 1)
        i2c_response[0] = (i2c_response[0] << 1) & 255
        i2c_response[0] = i2c_response[0] >> 4
        return (i2c_response[0] + 1) * 5

    def change_measurement_resolution(self, meas_res_temp, meas_res_hum):   #8 - 14 Bit
        """change the resolution of the measurements"""
        if (7 < meas_res_temp < 15) & (7 < meas_res_hum < 15):
            send_byte = ((meas_res_hum - 8) << 3) + (meas_res_temp - 8)
            self.wire_write(
                [(HTE501_COMMAND_READ_WRITE_SENSOR_SETTINGS >> 8),
                 (HTE501_COMMAND_READ_WRITE_SENSOR_SETTINGS & 0xFF),
                 HTE501_REGISTER_MEASUREMENT_RESOLUTION,
                 send_byte, calc_crc8([0x0F, send_byte], 0, 2)])
        else:
            raise Warning(get_status_string(6))

    def read_measurement_resolution(self):
        """reads the resolution of the measurements"""
        i2c_response = self.wire_write_read([
            (HTE501_COMMAND_READ_WRITE_SENSOR_SETTINGS >> 8),
            (HTE501_COMMAND_READ_WRITE_SENSOR_SETTINGS & 0xFF),
            HTE501_REGISTER_MEASUREMENT_RESOLUTION], 1)
        i2c_response2 = i2c_response[0]
        i2c_response[0] = (i2c_response[0] << 2) & 255
        i2c_response[0] = i2c_response[0] >> 5
        i2c_response2 = (i2c_response2 << 5) & 255
        i2c_response2 = i2c_response2 >> 5
        return i2c_response2 + 8, i2c_response[0] + 8

    def start_periodic_measurement(self):
        """starts the periodic measurement"""
        self.wire_write([(HTE501_COMMAND_START_PERIODIC_MEASUREMENT >> 8),
                         (HTE501_COMMAND_START_PERIODIC_MEASUREMENT & 0xFF)])

    def end_periodic_measurement(self):
        """ends the periodic measurement"""
        self.wire_write([(HTE501_COMMAND_END_PERIODIC_MEASUREMENT >> 8),
                          (HTE501_COMMAND_END_PERIODIC_MEASUREMENT & 0xFF)])

    def heater_on(self):
        """turns the heater on """
        self.wire_write([(HTE501_COMMAND_HEATER_ON >> 8),
                          (HTE501_COMMAND_HEATER_ON & 0xFF)])

    def heater_off(self):
        """turns the heater off"""
        self.wire_write([(HTE501_COMMAND_HEATER_OFF >> 8),
                          (HTE501_COMMAND_HEATER_OFF & 0xFF)])

    def read_identification(self):
        """reads the identification number"""
        i2c_response = self.wire_write_read(
            [(HTE501_COMMAND_READ_IDENTIFICATION >> 8),
             (HTE501_COMMAND_READ_IDENTIFICATION & 0xFF)], 9)
        if i2c_response[8] == calc_crc8(i2c_response, 0, 8):
            return i2c_response
        else:
            raise Warning(get_status_string(2))

    def reset(self):
        """resets the sensor"""
        self.wire_write([(HTE501_COMMAND_SOFT_RESET >> 8),
                         (HTE501_COMMAND_SOFT_RESET & 0xFF)])

    def new_measurement_ready(self):
        """get information if a new measurement is ready"""
        i2c_response = self.wire_write_read(
            [(HTE501_COMMAND_READ_REGISTER_2 >> 8),
             (HTE501_COMMAND_READ_REGISTER_2 & 0xFF)], 3)
        if i2c_response[2] == calc_crc8(i2c_response, 0, 2):
            return i2c_response[0] >> 7
        else:
            raise Warning(get_status_string(2))

    def constant_heater_on_off(self):
        """get the informatio if the heater is on or off"""
        i2c_response = self.wire_write_read(
            [(HTE501_COMMAND_READ_REGISTER_1 >> 8),
             (HTE501_COMMAND_READ_REGISTER_1 & 0xFF)], 3)
        if i2c_response[2] == calc_crc8(i2c_response, 0, 2):
            i2c_response[0] = (i2c_response[0] << 2) & 255
            return i2c_response[0] >> 7
        else:
            raise Warning(get_status_string(2))

    def clear_statusregister_1(self):
        """clear the status register 1"""
        self.wire_write([(HTE501_COMMAND_CLEAR_REGISTER_1 >> 8),
                         (HTE501_COMMAND_CLEAR_REGISTER_1 & 0xFF)])

    def wire_write_read(self,  buf, receiving_bytes):
        """write a command to the sensor to get different answers like temperature values,..."""
        write_command = i2c_msg.write(self.i2c_address, buf)
        read_command = i2c_msg.read(self.i2c_address, receiving_bytes)
        with SMBus(1) as hte501_communication:
            hte501_communication.i2c_rdwr(write_command, read_command)
        return list(read_command)

    def wire_write(self, buf):
        """write to the sensor"""
        write_command = i2c_msg.write(self.i2c_address, buf)
        with SMBus(1) as hte501_communication:
            hte501_communication.i2c_rdwr(write_command)