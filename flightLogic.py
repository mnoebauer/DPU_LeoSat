import asyncio
from drivers import heartbeat, ms5637, rtc
import getSensorData
import pandas as pd
import csv

def __main__():
    asyncio.run((mainFlightLogic()))

async def mainFlightLogic():
    """
    This is the main logic running during the whole flight
    First it calls the boot logic and creates referance values
    It constantly runs the heartbeat to show the watchdog that it is alive
    It constantly gets the sensor data and saves it
    """

    bootLogic() #running boot logic to update the reference values

    highPriorityTasks = []
    highPriorityTasks.append(asyncio.create_task(heartbeat.heartbeart.run())) #Starting the Heartbeat to show the Watchdog that the DPU is running

    mainTasks = []
    mainTasks.append(asyncio.create_task(getSensorData.DataScraper.collectData())) #Start collecting and saving sensor Data

    #following loop runs constanly
    #TO DO while true loop for transmisson, height, etc...


def bootLogic():
    """
    Boot Logic is called first on Boot,
    there is will be a reference for the altitude set
    and the time set to 00:00:00, also it records how many times 
    the DPU got booted up
    """

    f = open('data/bootcycles.txt','r') #opening the startAltitude text file in write mode
    bootnumber = f.readline()
    f.close()

    #0 is the initial value at the start
    if bootnumber == 0:
        rtc.RTC.set() #on first boot set time to 00:00:00
        altitude = ms5637.ms5637.read() #reading altitude on first boot to get reference
        f = open('data/startAltitude.txt','w')
        f.write(altitude)
        f.close()
    
    #old bootnumber +1 because there was one
    f = open('data/bootcycles.txt','w')
    newBootnumber = bootnumber + 1
    f.write(newBootnumber)
    f.close()

    #wrtiting csv headers if not done yet
    df = pd.read_csv("data/data.csv")
    if df.empty:
        with open('data/data.csv','w') as file:
            writer = csv.writer(file)
            writer.writerow(["Zeit", "Temperatur", "Luftdruck", "Luftfeuchtigkeit", "CPU-Temperatur", "Speichernutzung", "CPU-Last", "Error-Counter"])
