from lib import hte501_i2c_library

class HTE():
    """
    Driver for the HTE501 temperature, humidity and dewpoint sensor
    """
    def __init__(self,i2cadr):
        self.i2cadr = i2cadr
    
    def read(self):
        hte = hte501_i2c_library.HTE501(self.i2cadr)
        return self.hte.get_single_shot_temp_hum()