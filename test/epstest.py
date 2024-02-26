from smbus import SMBus
from time import sleep
addr = 0x70 # bus address
bus = SMBus(1) # indicates /dev/ic2-1
 
numb = 1
 

bus.write_byte(addr, 1) # switch it on
print("done")

sleep(5)

while True:
    b = bus.read_byte(addr)
    print(str(b))