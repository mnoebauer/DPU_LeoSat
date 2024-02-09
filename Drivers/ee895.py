from lib import ee895_i2c_library

class ee895:
    def read():
        sensor = ee895_i2c_library.EE895()
        sensor.trigger_new_measurement()
        temp = sensor.get_temp_c()
        c02 = sensor.get_co2_aver_with_pc()
        pressure = sensor.get_pressure_mbar()
        
        return temp,c02,pressure

