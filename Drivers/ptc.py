from smbus import SMBus
import time

i2c = SMBus(1)
i2cadress = 0x48

b = i2c.read_byte_data(i2cadress,0x01,)
print(str(b))