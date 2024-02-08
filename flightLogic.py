import asyncio
from Drivers import heartbeat, ms5637
import getSensorData

def __main__():
    asyncio.run((mainFlightLogic()))

async def mainFlightLogic():
    """
    This is the main logic running during the whole flight
    It constantly runs the heartbeat to show the watchdog that it is alive
    It constantly gets the sensor data and saves it
    """
    bootLogic() #running boot logic to update the reference values

    highPriorityTasks = []
    highPriorityTasks.append(asyncio.create_task(heartbeat.heartbeart.run())) #Starting the Heartbeat to show the Watchdog that the DPU is running

    mainTasks = []
    mainTasks.append(asyncio.create_task(getSensorData.DataScraper.collectData())) #Start collecting and saving sensor Data

def bootLogic():
    altitude = ms5637.ms5637.read()
    
    f = open('data/systemlog.txt','w') #opening the startAltitude text file in write mode
    f.write(altitude) #writing current alitude to file
    f.close() #closing file

