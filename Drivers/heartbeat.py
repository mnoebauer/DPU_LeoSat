import board
import time
import RP.GPIO as GPIO
import asyncio

class heartbeart():
    def __init__(self) -> None:
        GPIO.setmode(GPIO.Board)
        GPIO.setup(17,GPIO.OUT,initial = GPIO.LOW)

    async def run():
        while True:
            GPIO.output(17,1)
            await asyncio.sleep(0.5)
            GPIO.output(17,0)
            await asyncio.sleep(120)