import smbus2 as SMBus
from time import sleep

epsAdr = 0x80
SMBus = SMBus(1)
while True:

    with SMBus as bus:
        epsData = bus.read_i2c_block_data(epsAdr,0,5)
    
    print(str(epsData))
    sleep(3)