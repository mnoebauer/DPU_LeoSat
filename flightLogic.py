import sys
sys.path
import asyncio
from Drivers import heartbeat, ms5637, rtc
import getSensorData
import csv

async def mainFlightLogic():
    """
    This is the main logic running during the whole flight
    First it calls the boot logic and creates referance values
    It constantly runs the heartbeat to show the watchdog that it is alive
    It constantly gets the sensor data and saves it
    """

    mainTasks = []
    cameraTasks = []
    heartbeatObj = heartbeat.heartbeart()
    ms5637Obj = ms5637.ms5637()

    task = asyncio.create_task(bootLogic()) #running boot logic
    await asyncio.wait_for(task,5)

    #mainTasks.append(asyncio.create_task(heartbeatObj.run())) #Starting the Heartbeat to show the Watchdog that the DPU is running
    mainTasks.append(asyncio.create_task(getSensorData.DataScraper.collectData())) #Start collecting and saving sensor data

    f = open('Desktop/DPU_LeoSat/data/startaltitude.txt','r') #open startAltitude file in read mode
    startAltitude = f.read()
    sAltitude = float(startAltitude)
    f.close()

    #following loop runs constanly
    while True:
        #calculate rAltitude(risen altitude) =  (cAltitude(currentAltitude) - sAltitude(startAltitude))
        cAltitude = ms5637Obj.read()
        rAltitude = cAltitude - sAltitude

        #Check risen Altitude for camera mode
        if rAltitude < 1000 or rAltitude > 34000:
            print("bla")
            #start video recording if not already running

        else:
            print("blu")
            #run continous picture taking task

        await asyncio.sleep(60) #refresh

async def bootLogic():
    """
    Boot Logic is called first on Boot,
    there is will be a reference for the altitude set
    and the time set to 00:00:00, also it records how many times 
    the DPU got booted up
    """
    ms5637Obj = ms5637.ms5637()
    rtcObj = rtc.RTC()

    f = open('Desktop/DPU_LeoSat/data/bootcycles.txt','r') #opening the bootcycles file in read mode
    bootnumber = f.readline()
    f.close()

    #if it is the first boot, save the current altitude, reset the rtc and fill the headings of the csv
    if int(bootnumber) == 0:
        altitude = ms5637Obj.read() #reading altitude on first boot to get reference
        f = open('Desktop/DPU_LeoSat/data/startaltitude.txt','w')
        f.write(str(altitude))
        f.close()
        rtcObj.set() #Setting the rtc to 00:00:00

        #Filling the first row of the csv file with the names of the data
        with open('Desktop/DPU_LeoSat/data/data.csv','w') as file:
            writer = csv.writer(file)
            writer.writerow(["Zeit", "Gas-Resistance_BME688", "Temperature_BME688", "Humidity_BME688", "Pressure_BME688", "Temperatur_HTE501_Inside", "Humidity_HTE501_Inside",
                             "Temperatur_HTE501_Outside", "Humidity_HTE501_Outside",
                              "X-Acceleration", "Y-Acceleration", "Z-Acceleration",
                              "Altitude_MS5637", "Latitude", "Longitude", "Altitude_GPS", "Temperature_EE895", "Co2_EE895", "Pressure_EE895"])

    #old bootnumber +1
    f = open('Desktop/DPU_LeoSat/data/bootcycles.txt','w')
    newBootnumber = int(bootnumber) + 1
    f.write(str(newBootnumber))
    f.close()

def main():
    asyncio.run((mainFlightLogic()))

if __name__ == '__main__':
    main()