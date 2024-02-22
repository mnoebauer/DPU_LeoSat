import smbus2 as SMBus
from time import sleep

epsAdr = 0x80

while True:
    with SMBus(1) as bus:
        epsData = bus.read_i2c_block_data(epsAdr,0,5)
    
    print(str(epsData))
    sleep(3)