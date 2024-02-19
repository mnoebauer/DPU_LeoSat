from smbus import SMBus
import time

i2c = SMBus(1)

i2cadress = 0x48
temp3 = bytearray(3)

i2c.readfrom_into(i2cadress,temp3)
results, status = temp3[0] << 8 | temp3[1], temp3[2]

print(str(results))
