import board
import time
import bme680
import adafruit_ds3231

errorcounter = 0

def initializeAll():
    writeTextToLog('Starting:       Initialisation of Sensors')
    try:
        initBME688()
    except:
        writeTextToLog('Failed:     Initialisation of Sensors')
        errorCounter += 1
    finally:
        writeTextToLog('Success:     Initialisation of Sensors') 

def initBME688():
    writeTextToLog('Starting:       Initialisation BME688')
    global sensor_bme680
    try:
        bme688 = bme680.BME680(bme680.I2C_ADDR_SECONDARY)    
        bme688.set_humidity_oversample(bme680.OS_8X)
        bme688.set_pressure_oversample(bme680.OS_8X)
        bme688.set_temperature_oversample(bme680.OS_8X)
        bme688.set_filter(bme680.FILTER_SIZE_3)
    except:
        writeTextToLog('Failed:     Initialisation BME688')
        errorCounter += 1
    else:
        writeTextToLog("Success:        Initialisation BME688")

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
    f.write(" " + a) #writing the content into the file

def main():
    initRTC()
    writeTextToLog('Succesfull:     Initializing RTC')
    writeTextToLog('Starting:     Boot')
    initializeAll()

         
if __name__ == "__main__":
    main()