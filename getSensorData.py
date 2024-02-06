import csv
from Drivers import bma400, HTE501, ms5637, rtc

data = []

class DataSaver:

    async def collectData():
        global data
        while True:
            try:
                data.append(HTE501.HTE.read())
            except:
                writeToLog("HTE501 Reading failed")
            
            try:
                data.append(bma400.bma400.read())
            except:
                print("BMA400 reading failed")

            try:
                data.append(ms5637.ms5637.read())
            except:
                print("MS5637 reading failed")


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
        
