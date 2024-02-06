import asyncio
from Drivers import ms5637, bma400
from Drivers import heartbeat

def __main__():
    asyncio.run(logic())

async def logic():
    tasks = []
    tasks.append(asyncio.create_task(heartbeat.heartbeart.run()))

async def gatherData():
    dataTasks = []
    dataTasks.append()