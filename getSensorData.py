import csv
import asyncio
from Drivers import bma400, HTE501, ms5637, rtc, bme688

data = []

class DataScraper:
    """
    This class is fetches all the data from the sensors and saves it to the csv file
    """
    async def collectData():
        global data
        while True:
            try:
                data.append(bme688.BME680.read())
            except:
                writeToLog("BME688 reading failed")
                data.append("NaN")
            
            try:
                data.append(HTE501.HTE.read())
            except:
                writeToLog("HTE501 reading failed")
                data.append("NaN")
        
            try:
                data.append(bma400.bma400.read())
            except:
                writeToLog("BMM400 reading failed")
                data.append("NaN")

            try:
                data.append(ms5637.ms5637.read())
            except:
                writeToLog("Ms5637 reading fialed")
                data.append("NaN")


            asyncio.sleep(3)

def writeToLog(x):
       t = rtc.RTC.read()
       f = open('data/systemlog.txt','a') #opening the systemlog text file in append mode
       f.write('\n') #creating a new line for every entry
       f.write(t) #documenting the time on every entry
       f.write(x) #writing the content into the file 
    
def writeCsvData():
    global data
    with open('data/data.csv','a') as file:
        writer = csv.writer(file)
        writer.writerow(data)        
