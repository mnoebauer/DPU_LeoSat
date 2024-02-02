import board
import time
import bme680
import adafruit_ds3231
import csv
from hte501_i2c_library import HTE501
import bma400

def initBMA400():
    global mbma400
    writeTextToLog('Starting:       Initialisation BMA400')
    try:
        i2c = board.I2C()
        mbma400 = bma400.BMA400(i2c)
    except:
        writeTextToLog('Failed:       Initialisation BMA400')

def readBMA400():
    global accx,accy,accz
    writeTextToLog('Starting:       Reading BMA400')
    try:
        accx, accy, accz = mbma400.acceleration
    except:
        writeTextToLog('Failed:       Reading BMA400')

def initHTE501():
    global HTE_501
    writeTextToLog('Starting:       Initialisation HTE501')
    try:
        HTE_501 = HTE501(0x40)
    except:
        writeTextToLog('Failed:       Initialisation HTE501')

def readHTE501():
    global temperature_hte501, humidity_hte501, dewpoint
    writeTextToLog('Starting:       Reading HTE501')
    try:
        temperature_hte501,humidity_hte501 = HTE_501.get_single_shot_temp_hum()
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
    global temp, p, h
    writeTextToLog('Starting:       Reading BME688')
    try:
        if sensor_bme680.get_sensor_data():
            temp = sensor_bme680.data.temperature
            p = sensor_bme680.data.pressure
            h = sensor_bme680.data.humidity
    except:
        writeTextToLog('Failed:      Reading BME688')

def readAll():
    writeTextToLog('Starting:       Reading Sensor Data')
    try:
        readBME688()
        readHTE501()
        readBMA400()
    except:
        writeTextToLog('Failed:       Reading Sensor Data')

def initializeAll():
    writeTextToLog('Starting:       Initialisation of Sensors')
    try:
        initCsvFile()
        initBME688()
        initHTE501()
        initBMA400()
    except:
        writeTextToLog('Failed:     Initialisation of Sensors')

def initCsvFile():
    writeTextToLog('Starting:     Initialising CSV File')
    try:
        with open('data/data.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(["Zeit", "Temperatur", "Luftdruck", "Luftfeuchtigkeit", "CPU-Temperatur", "Speichernutzung", "CPU-Last", "Error-Counter"])
    except:
        writeTextToLog('Failed:     Initialising CSV File')
        
def writeCsvData():
    writeTextToLog('Starting:     Writing CSV File')
    time = getTime()
    try:
        with open('data.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow([time, temp,temperature_hte501, p, h, dewpoint, accx, accy, accz])
    except:
        writeTextToLog('Failed:     Writing to CSV File') 

def initRTC():
    global rtc #setting rtc variable global so it can be used everywhere
    i2c = board.I2C()  
    rtc = adafruit_ds3231.DS3231(i2c)   
    rtc.datetime = time.struct_time((2024,0,0,0,0,0,0,1,-1)) #setting the hours to 0 to get the start time

def getTime():
    r = rtc.datetime
    t = str(r.tm_hour) +":"+ str(r.tm_min)+":"+ str(r.tm_sec)
    return t

def writeTextToLog(a):
    t = rtc.datetime
    f = open('data/systemlog.txt','a') #opening the systemlog text file in append mode
    f.write('\n') #creating a new line for every entry
    f.write(getTime()) #documenting the time on every entry
    f.write(a) #writing the content into the file

def main():
    initRTC()
    writeTextToLog('Succesfull:     Initializing RTC')
    writeTextToLog('Starting:     Boot')
    initializeAll()
    while(1):
        readAll()
        writeCsvData()
         
if __name__ == "__main__":
    main()