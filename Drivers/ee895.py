from lib import ee895_i2c_library

class ee895:
    sensor = ee895_i2c_library.EE895()

    def read(self):

        self.sensor.trigger_new_measurement()

        temp = self.sensor.get_temp_c()
        c02 = self.sensor.get_co2_aver_with_pc()
        pressure = self.sensor.get_pressure_mbar()
        
        return temp,c02,pressure

