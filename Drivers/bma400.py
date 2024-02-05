import bma400
import board

class bma400():
    i2c = board.I2C()
    
    def read():
        mbma = bma400.BMA400()
        return mbma.acceleration
