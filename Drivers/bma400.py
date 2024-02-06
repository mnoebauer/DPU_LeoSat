import bma400
import board

class bma400():
    """
    Driver for the Bosch BMA400 acceleration sensor
    """
    def read():
        i2c = board.I2C()
        mbma = bma400.BMA400(i2c)
        return mbma.acceleration
