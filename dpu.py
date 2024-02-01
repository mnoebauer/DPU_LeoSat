import board
import time
import bme680
import adafruit_ds3231

data = []

def readAll():
    global errorcounter
    writeTextToLog('Starting:       Reading Sensor Data')
    try:
        readBME688()
    except:
        writeTextToLog('Failed:       Reading Sensor Data')

    finally:
        writeTextToLog('Starting:       Reading Sensor Data')

def initializeAll():
    global errorcounter
    writeTextToLog('Starting:       Initialisation of Sensors')
    try:
        initBME688()

    except:
        writeTextToLog('Failed:     Initialisation of Sensors')

    finally:
        writeTextToLog('Success:     Initialisation of Sensors') 

def initBME688():
    writeTextToLog('Starting:       Initialisation BME688')
    global bme688, errorcounter
    try:
        bme688 = bme680.BME680(bme680.I2C_ADDR_SECONDARY)   #initializing the bme688 with the secondary i2c adress
        bme688.set_humidity_oversample(bme680.OS_8X)
        bme688.set_pressure_oversample(bme680.OS_8X)
        bme688.set_temperature_oversample(bme680.OS_8X)
        bme688.set_filter(bme680.FILTER_SIZE_3)
    except:
        writeTextToLog('Failed:     Initialisation BME688')

    else:
        writeTextToLog("Success:        Initialisation BME688")

def readBME688():
    global errorcounter
    writeTextToLog('Starting:       Reading BME688')
    try:
        if bme688.get_sensor_data():
            temperatur = bme688.data.temperature
            pressure = bme688.data.pressure
            humidity = bme688.data.humidity
            data.append(temperatur,pressure,humidity)
    except:
        writeTextToLog('Failed:      Reading BME688')

    finally:
        writeTextToLog('Success:        Reading BME688')

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