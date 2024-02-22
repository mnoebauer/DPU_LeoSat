from smbus import SMBus
 
addr = 0x70 # bus address
bus = SMBus(1) # indicates /dev/ic2-1
 
numb = 1
 

bus.write_byte(addr, 1) # switch it on
print("done")

while True:
    b = bus.read_byte_data(addr,5)
    print(str(b))