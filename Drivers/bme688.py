import bme680

class BME680:
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY) 
    sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
    sensor.set_humidity_oversample(bme680.OS_2X)
    sensor.set_pressure_oversample(bme680.OS_4X)
    sensor.set_temperature_oversample(bme680.OS_8X)
    
    def read(self):
        if self.sensor.get_sensor_data():
            gas = self.sensor.data.gas_resistance
            temp = self.sensor.data.temperature
            hum = self.sensor.data.humidity
            pres = self.sensor.data.pressure

        else:
            gas = "NaN"
            temp = "NaN"
            hum = "NaN"
            pres = "NaN"

        return gas,temp,hum,pres