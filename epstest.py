from smbus2 import SMBus

with SMBus(1) as bus:
    b = bus.read_byte(0x80)
    print(b)