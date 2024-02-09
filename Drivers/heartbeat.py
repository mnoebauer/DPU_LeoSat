import board
import asyncio
import time
import RPi.GPIO as GPIO

class heartbeart:
    """
    Driver class for the "Hearbeat" that sends a signal every 2 Minutes 
    to the Watchdog that the DPU is still alive
    """
    t = GPIO
    t.setmode(t.Board)
    t.setup(17,t.OUT,initial = t.LOW)

    async def run(self):
        while True:
            self.t.output(17,1)
            await asyncio.sleep(0.5)
            self.t.output(17,0)
            await asyncio.sleep(120)