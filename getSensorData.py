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
        b400 = bma400.bma400()
        m5637 = ms5637.ms5637()

        while True:
            #reading time
            try:
                data.append(rtc.RTC.read())
            except:
                writeToLog("RTC reading failed")
                data.append("NaN")

            #reading gas resistance
            try:
                data.append(bme688.BME680.read())
            except:
                writeToLog("BME688 reading failed")
                data.append("NaN")
            
            #reading temperature and humidity
            try:
                temp,hum = HTE501.HTE.read()
                data.append(temp)
                data.append(hum)
            except:
                writeToLog("HTE501 reading failed")
                data.append("NaN")
                data.append("NaN")

            #reading x,y,z acceleration
            try:
                accx,accy,accz = bma400.bma400.read()
                data.append(accx)
                data.append(accy)
                data.append(accz)
            except:
                writeToLog("BMM400 reading failed")
                data.append("NaN")

            #reading altitude
            try:
                data.append(m5637.read())
            except:
                writeToLog("Ms5637 reading failed")
                data.append("NaN")

            try:
                data.append(gps.GPS.read())
            except:
                writeToLog("GPS reading failed")
                data.append("NaN")
                data.append("NaN")
                data.append("NaN")
            
            try:
                data.append(ee895.ee895.read())
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
