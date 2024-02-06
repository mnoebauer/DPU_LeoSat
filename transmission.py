import board
import asyncio
import RPi.GPIO as GPIO

class Transmission:

    def send():
        """
        send function
        """

async def activateCom():
    GPIO.setmode(GPIO.Board)
    GPIO.setup(27,GPIO.OUT,initial = GPIO.LOW)

    GPIO.output(27,1)
    await asyncio.sleep(1)
    GPIO.output(27,0)

async def waitForResponse():
    GPIO.setmode(GPIO.Board)
    GPIO.setup(27,GPIO.IN)

