from lib import hte501_i2c_library

class HTE():
    """
    Driver for the HTE501 temperature, humidity and dewpoint sensor
    """
    def read():
        hte = hte501_i2c_library.HTE501(0x40)
        return hte.get_single_shot_temp_hum