from smbus2 import SMBus
bus = SMBus(1)

b = bus.read_byte(0x80)
print(b)