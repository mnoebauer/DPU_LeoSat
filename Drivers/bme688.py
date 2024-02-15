import bme680

class BME680:
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY) 
    sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
    
    def read(self):
        if self.sensor.get_sensor_data():
            gas = self.sensor.data.gas_resistance
        else:
            gas = "NaN"
        return gas