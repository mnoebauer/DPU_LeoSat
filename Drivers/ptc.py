import ads1110
from machine import I2C

i2c = I2C(freq = 100000)

ads = ads1110.ADS1110()

b = ads.read(ads1110._DR_15SPS,ads1110._PGA_1)

print(str(b))