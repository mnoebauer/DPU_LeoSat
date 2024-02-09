import sys
sys.path

import asyncio
from Drivers import heartbeat, ms5637, rtc
import getSensorData
#import warnings
#warnings.simplefilter(action='ignore', category=FutureWarning)
#import pandas as pd
import csv



async def mainFlightLogic():
    """
    This is the main logic running during the whole flight
    First it calls the boot logic and creates referance values
    It constantly runs the heartbeat to show the watchdog that it is alive
    It constantly gets the sensor data and saves it
    """

    highPriorityTasks = []
    mainTasks = []
    cameraTasks = []
    heartbeatObj = heartbeat.heartbeart()
    ms5637Obj = ms5637.ms5637()

    bootLogic() #running boot logic

    highPriorityTasks.append(asyncio.create_task(heartbeatObj.run())) #Starting the Heartbeat to show the Watchdog that the DPU is running
    mainTasks.append(asyncio.create_task(getSensorData.DataScraper.collectData())) #Start collecting and saving sensor data

    f = open('data/startaltitude.txt','r') #open startAltitude file in read mode
    startAltitude = f.read()
    print("startaltitude:"+ startAltitude)
    sAltitude = int(startAltitude)
    f.close()

    #following loop runs constanly
    while True:
        #calculate rAltitude(risen altitude) =  (cAltitude(currentAltitude) - sAltitude(start Altitude))
        cAltitude = ms5637Obj.read()
        rAltitude = cAltitude - sAltitude

        #camera mode 
        if rAltitude < 1000 or rAltitude > 34000:
            print("bla")
            #start video recording if not already running

        else:
            print("blu")
            #run continous picture taking task

        await asyncio.sleep(60) #refresh

def bootLogic():
    """
    Boot Logic is called first on Boot,
    there is will be a reference for the altitude set
    and the time set to 00:00:00, also it records how many times 
    the DPU got booted up
    """
    ms5637Obj = ms5637.ms5637()

    f = open('data/bootcycles.txt','r') #opening the startAltitude file in read mode
    bootnumber = f.readline()
    print("bootnumber:"+bootnumber)
    f.close()

    #0 is the initial value at the start, during the launch it should be the first boot
    altitude = ms5637Obj.read() #reading altitude on first boot to get reference
    f = open('data/startaltitude.txt','w')
    f.write(altitude)
    f.close()
    """
    if bootnumber == 0:
        print("In?")
        #rtc.RTC.set() #on first boot set time to 00:00:00
        
        """
"""  
    #old bootnumber +1 because there was one
    f = open('data/bootcycles.txt','w')
    newBootnumber = int(bootnumber) + 1
    f.write(str(newBootnumber))
    f.close()

    #wrtiting csv headers if not done yet
    df = pd.read_csv("data/data.csv")
    if df.empty:
        with open('data/data.csv','w') as file:
            writer = csv.writer(file)
            writer.writerow(["Zeit", "Gas-Resistance", "Temperatur", "Luftfeuchtigkeit", "X-Acceleration", "Y-Acceleration", "Z-Acceleration",
                              "Altitude", "Latitude", "Longitude", "Altitude_GPS", "Temperature_EE895", "Co2_EE895", "Pressure_EE895"])
"""

def main():
    asyncio.run((mainFlightLogic()))

if __name__ == '__main__':
    main()