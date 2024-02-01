import board
import time
import bme680
import adafruit_ds3231
from hte501_i2c_library import HTE501

def initHTE501():
    global HTE_501
    writeTextToLog('Starting:       Initialisation HTE501')
    try:
        HTE_501 = HTE501(0x40)
    except:
        writeTextToLog('Failed:       Initialisation HTE501')

def readHTE501():
    writeTextToLog('Starting:       Reading HTE501')
    try:
        temperature,humidity = HTE_501.get_single_shot_temp_hum()
        dewpoint = HTE_501.get_dewpoint()
    except:
        writeTextToLog('Failed:       Reading HTE501')

def initBME688():
    writeTextToLog('Starting:       Initialisation BME688')
    global sensor_bme680
    try:
        sensor_bme680 = bme680.BME680(bme680.I2C_ADDR_SECONDARY)   #initializing the bme688 with the secondary i2c adress
        sensor_bme680.set_humidity_oversample(bme680.OS_8X)
        sensor_bme680.set_pressure_oversample(bme680.OS_8X)
        sensor_bme680.set_temperature_oversample(bme680.OS_8X)
        sensor_bme680.set_filter(bme680.FILTER_SIZE_3)
    except:
        writeTextToLog('Failed:     Initialisation BME688')

def readBME688():
    writeTextToLog('Starting:       Reading BME688')
    try:
        if sensor_bme680.get_sensor_data():
            temperatur = sensor_bme680.data.temperature
            pressure = sensor_bme680.data.pressure
            humidity = sensor_bme680.data.humidity
    except:
        writeTextToLog('Failed:      Reading BME688')

def readAll():
    writeTextToLog('Starting:       Reading Sensor Data')
    try:
        readBME688()
        readHTE501()
    except:
        writeTextToLog('Failed:       Reading Sensor Data')

def initializeAll():
    writeTextToLog('Starting:       Initialisation of Sensors')
    try:
        initBME688()
        initHTE501()
    except:
        writeTextToLog('Failed:     Initialisation of Sensors')

def initRTC():
    global rtc #setting rtc variable global so it can be used everywhere
    i2c = board.I2C()  
    rtc = adafruit_ds3231.DS3231(i2c)   
    rtc.datetime = time.struct_time((2024,0,0,0,0,0,0,1,-1)) #setting the hours to 0 to get the start time

def writeTextToLog(a):
    t = rtc.datetime
    f = open('data/systemlog.txt','a') #opening the systemlog text file in append mode
    f.write('\n') #creating a new line for every entry
    f.write(str(t.tm_hour)+":"+ str(t.tm_min)+":"+ str(t.tm_sec)) #documenting the time on every entry
    f.write(a) #writing the content into the file

def main():
    initRTC()
    writeTextToLog('Succesfull:     Initializing RTC')
    writeTextToLog('Starting:     Boot')
    initializeAll()
    readAll()
         
if __name__ == "__main__":
    main()