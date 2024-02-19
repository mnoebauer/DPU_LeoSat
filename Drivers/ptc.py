from smbus import SMBus
import time

i2c = SMBus(1)
i2cadress = 0x48

b = i2c.read_byte(i2cadress)

print(str(b))
