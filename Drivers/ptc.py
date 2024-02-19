import board
import busio


i2c = busio.I2C(board.SCL, board.SDA)

i2cadress = 0x48
temp3 = bytearray(3)

i2c.readfrom_into(i2cadress,temp3)
results, status = temp3[0] << 8 | temp3[1], temp3[2]

temp = (results & 0x10000)/16

print(str(results))
print(str(status))
print(str(temp))
