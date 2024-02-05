import asyncio
from Drivers import ms5637, bma400

async def flightStageEstimation():
   """
   0... Grounded
   1... Starting
   2... Rising
   3... Freefall
   4...Parachute
   """
   alt = ms5637.ms5637.read()
   accx,acc,y,accz = bma400.bma400.read()

   


   