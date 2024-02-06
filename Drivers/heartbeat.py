import board
import asyncio
import time
import RP.GPIO as GPIO

class heartbeart():
    """
    Driver class for the "Hearbeat" that sends a signal every 2 Minutes 
    to the Watchdog that the DPU is still alive
    """
    def __init__(self) -> None:
        GPIO.setmode(GPIO.Board)
        GPIO.setup(17,GPIO.OUT,initial = GPIO.LOW)

    async def run():
        while True:
            GPIO.output(17,1)
            await asyncio.sleep(0.5)
            GPIO.output(17,0)
            await asyncio.sleep(120)