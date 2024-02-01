import board
import time
import bme680
import adafruit_ds3231
from hte501_i2c_library import HTE501

data = []

def initHTE501():
    global HTE_501
    HTE_501 = HTE501(0x40)

def readHTE501():
    try:
        temperature,humidity = HTE_501.get_single_shot_temp_hum()
        dewpoint = HTE_501.get_dewpoint()

    except:
        writeTextToLog('Failed:       HTE501')

    finally:
        writeTextToLog('Success:       HTE501')

def initBME688():
    writeTextToLog('Starting:       Initialisation BME688')
    global sensor_bme680, errorcounter
    try:
        sensor_bme680 = bme680.BME680(bme680.I2C_ADDR_SECONDARY)   #initializing the bme688 with the secondary i2c adress
        sensor_bme680.set_humidity_oversample(bme680.OS_8X)
        sensor_bme680.set_pressure_oversample(bme680.OS_8X)
        sensor_bme680.set_temperature_oversample(bme680.OS_8X)
        sensor_bme680.set_filter(bme680.FILTER_SIZE_3)
    except:
        writeTextToLog('Failed:     Initialisation BME688')

    else:
        writeTextToLog("Success:        Initialisation BME688")

def readBME688():
    global errorcounter, data
    writeTextToLog('Starting:       Reading BME688')
    try:
        if sensor_bme680.get_sensor_data():
            temperatur = sensor_bme680.data.temperature
            pressure = sensor_bme680.data.pressure
            humidity = sensor_bme680.data.humidity
            data.append(temperatur,pressure,humidity)
    except:
        writeTextToLog('Failed:      Reading BME688')

    finally:
        writeTextToLog('Success:        Reading BME688')

def readAll():
    global errorcounter
    writeTextToLog('Starting:       Reading Sensor Data')
    try:
        readBME688()
        readHTE501()
    except:
        writeTextToLog('Failed:       Reading Sensor Data')

    finally:
        writeTextToLog('Starting:       Reading Sensor Data')

def initializeAll():
    global errorcounter
    writeTextToLog('Starting:       Initialisation of Sensors')
    try:
        initBME688()
        initHTE501()
    except:
        writeTextToLog('Failed:     Initialisation of Sensors')

    finally:
        writeTextToLog('Success:     Initialisation of Sensors') 

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