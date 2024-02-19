from lib import hte501_i2c_library

class HTE():
    """
    Driver for the HTE501 temperature, humidity and dewpoint sensor
    """
    adr = 0
    def __init__(self,i2cadr):
        self.i2cadr = self.i2cadr
        adr = self.i2cadr
    
    hte = hte501_i2c_library.HTE501(adr)
    
    def read(self):
        return self.hte.get_single_shot_temp_hum()