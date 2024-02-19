import csv
import asyncio
from Drivers import bma400, HTE501, ms5637, rtc, bme688, rtc, gps, ee895

data = []

class DataScraper:
    """
    This class is fetches all the data from the sensors and saves it to the csv file
    """
    async def collectData():
        global data

        rtcObj = rtc.RTC()
        bma400Obj = bma400.bma400()
        m5637Obj = ms5637.ms5637()
        bme688Obj = bme688.BME680()
        gpsObj = gps.GPS()
        hte501InsideObj = HTE501.HTE(0x40) #Object of hte501 class with the i2c adress for the inside sensor
        hte501OutsideObj = HTE501.HTE(0x20) #Object of hte501 class with the i2c adress for the outside sensor
        ee895Obj = ee895.ee895()

        while True:
            #reading time
            try:
                data.append(rtcObj.read())
            except:
                writeToLog("RTC reading failed")
                data.append("NaN")

            #reading gas resistance
            try:
                gas,temp_bme,hum_bme,pres_bme = bme688Obj.read()
                data.append(gas)
                data.append(temp_bme)
                data.append(hum_bme)
                data.append(pres_bme)

            except:
                writeToLog("BME688 reading failed")
                data.append("NaN")
            
            #reading temperature and humidity via HTE501 inside
            try:
                temp,hum = hte501InsideObj.read()
                data.append(temp)
                data.append(hum)
            except:
                writeToLog("HTE501 Inside reading failed")
                data.append("NaN")
                data.append("NaN")

            #reading temperature and humidity via HTE501 outside
            try:
                temp_o,hum_o = hte501OutsideObj.read()
                data.append(temp_o)
                data.append(hum_o)
            except:
                writeToLog("HTE501 Outside reading failed")
                data.append("NaN")
                data.append("NaN")

            #reading x,y,z acceleration
            try:
                accx,accy,accz = bma400Obj.read()
                data.append(accx)
                data.append(accy)
                data.append(accz)
            except:
                writeToLog("BMM400 reading failed")
                data.append("NaN")
                data.append("NaN")
                data.append("NaN")

            #reading altitude
            try:
                data.append(m5637Obj.read())
            except:
                writeToLog("Ms5637 reading failed")
                data.append("NaN")
            
            try:
                gpstup = gpsObj.read()
                data.append(gpstup[0])
                data.append(gpstup[1]) 
                data.append(gpstup[2]) 
            except:
                writeToLog("GPS reading failed")
                data.append("NaN")
                data.append("NaN")
                data.append("NaN")
            
            try:
                data.append(ee895Obj.read())
            except:
                writeToLog("EE895 reading failed")
                data.append("NaN")
                data.append("NaN")
                data.append("NaN")

            writeCsvData(data)
            data.clear()
            await asyncio.sleep(3)

def writeToLog(x):
       t = rtc.RTC()
       b = t.read()
       f = open('data/systemlog.txt','a') #opening the systemlog text file in append mode
       f.write('\n') #creating a new line for every entry
       f.write(b) #documenting the time on every entry
       f.write(x) #writing the content into the file 
    
def writeCsvData(d):
    with open('data/data.csv','a') as file:
        writer = csv.writer(file)
        writer.writerow(d)        
