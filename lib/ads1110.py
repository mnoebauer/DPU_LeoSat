# The MIT License (MIT)
#
# Copyright (c) 2017 Robert Hammelrath (@robert-hh)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
import time


_OS_MASK = const(0x80)
_OS_SINGLE = const(0x80)  # Write: Set to start a single-conversion
_OS_BUSY = const(0x80)    # Read: Bit=1 when conversion is in progress
_OS_NOTBUSY = const(0x00) # Read: Bit=0 when device is not performing a conversion

_PGA_MASK = const(0x03)
_PGA_1 = const(0x00)  # +/-2.048V range = Gain 1 (default)
_PGA_2 = const(0x01)  # +/-1.024V range = Gain 2
_PGA_4 = const(0x02)  # +/-0.512V range = Gain 4
_PGA_8 = const(0x03)  # +/-0.256V range = Gain 8

_MODE_MASK = const(0x010)
_MODE_CONTIN = const(0x00)  # Continuous conversion mode (default)
_MODE_SINGLE = const(0x10)  # Power-down single-shot mode

_DR_MASK = const(0x0C)    # 
_DR_240SPS = const(0x00)  # 240 samples per second, 12 Bits
_DR_60SPS = const(0x04)   # 60 samples per second, 14 Bits
_DR_30SPS = const(0x08)   # 30 samples per second, 15 Bits
_DR_15SPS = const(0x0C)   # 15 samples per second, 16 Bits (Default)

_GAINS = (
    _PGA_1, # 1x
    _PGA_2, # 2x
    _PGA_4, # 4x
    _PGA_8, # 8x
)

_RATES = (
    _DR_240SPS,# 240 samples per second
    _DR_60SPS, # 60 samples per second
    _DR_30SPS, # 30 samples per second
    _DR_15SPS  # 15 samples per second
)

class ADS1110:
    def __init__(self, i2c, address=0x48):
        self.i2c = i2c
        self.address = address
        self.temp1 = bytearray(1)
        self.temp3 = bytearray(3)

    def _write_config(self, config):
        self.temp1[0] = config
        self.i2c.writeto(self.address, self.temp1)

    def _read_data_config(self):
        self.i2c.readfrom_into(self.address, self.temp3)
        return ((self.temp3[0] << 8) | self.temp3[1], self.temp3[2])

    def read(self, rate, gain):
        """Read voltage at given rate.  Time depends on conversion rate."""
        self._write_config(_OS_SINGLE | _MODE_SINGLE |
            _RATES[rate] | _GAINS[gain])
        while True: 
            value, status = self._read_data_config() # read data
            if (status & _OS_MASK) == 0: # data flagged
                break
            time.sleep_ms(1)
        return value


