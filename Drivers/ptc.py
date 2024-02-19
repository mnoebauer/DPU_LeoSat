import quick2wire.i2c as i2c
import struct

address = 0x49     # Address for ADS1110A1
config_byte = 0x8C # what to fill the config register with (default 0x8C)

with i2c.I2CMaster() as bus:
	#configure the device with a non-default config byte
	#bus.transaction(i2c.write_bytes(address, config_byte))
	
	#Pulls the values from ADC buffer 
	#only retuns values from 1st (and only)  read in trasaction
	results = bus.transaction(i2c.reading(address,2))[0]

	#Convert the string returned from read to a short intiger
	results_parse = struct.unpack(">H", results)[0]
	
print(str(results_parse))