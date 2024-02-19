from smbus import SMBus
import time

i2c = SMBus(1)
i2cadress = 0x48

b = i2c.read_byte_data(i2cadress,0x01)
y = i2c.read_byte_data(i2cadress,0x02)
print(str(b))
print(str(y))