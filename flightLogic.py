import asyncio
from Drivers import ms5637, bma400
from Drivers import heartbeat
import getSensorData

def __main__():
    asyncio.run(())

async def mainFlightLogic():
    """
    This function will run when the first setup process is done
    It constantly gathers sensor data and saves that data
    """
    tasks = []
    tasks.append(asyncio.create_task(heartbeat.heartbeart.run())) #start Heartbeat to show Watchdog DPU is alive
    tasks.append(asyncio.create_task(getSensorData.DataScraper.collectData())) #start collecting and saving data
