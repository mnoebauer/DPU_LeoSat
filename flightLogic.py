import asyncio
from Drivers import ms5637, bma400
from Drivers import heartbeat
import getSensorData
import transmission

def __main__():
    asyncio.run((mainFlightLogic()))

async def mainFlightLogic():
    """
    This is the main logic running during the whole flight
    It constantly runs the heartbeat to show the watchdog that it is alive
    It constantly gets the sensor data and saves it
    """

    highPriorityTasks = []
    highPriorityTasks.append(asyncio.create_task(heartbeat.heartbeart.run())) #Starting the Heartbeat to show the Watchdog that the DPU is running

    mainTasks = []
    mainTasks.append(asyncio.create_task(getSensorData.DataScraper.collectData())) #Start collecting and saving sensor Data