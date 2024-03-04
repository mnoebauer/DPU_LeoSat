import board
import busio

class ptc():
    """
    Driver for the ADC ADS1110
    """

    i2c = busio.I2C(board.SCL, board.SDA)

    i2cadress = 0x48
    temp3 = bytearray(3)
        
    def read(self):
        self.i2c.readfrom_into(self.i2cadress,self.temp3)
        results, status = self.temp3[0] << 8 | self.temp3[1], self.temp3[2]

        temp = (results & 0xFFF)/16 #hex to decimal

        return results