from smbus import SMBus
 
addr = 0x10 # bus address
bus = SMBus(1) # indicates /dev/ic2-1
 
numb = 1
 
print ("Enter 1 for ON or 0 for OFF")
while numb == 1:
	print("in")
	bus.write_byte(addr, 1) # switch it on
	print("done")
