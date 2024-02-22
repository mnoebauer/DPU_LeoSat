import asyncio
import RPi.GPIO as GPIO

class heartbeart:
    """
    Driver class for the "Hearbeat" that sends a signal every 2 Minutes 
    to the Watchdog that the DPU is still alive
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17,GPIO.OUT)
    
    async def run(self):
        while True:
            GPIO.output(17,1)
            await asyncio.sleep(0.5)
            GPIO.output(17,0)
            await asyncio.sleep(20)