import board
import asyncio
import RPi.GPIO as GPIO

class Transmission:
    """
    Class for transmitting the data to the communication pcb
    """
    def send():
        """
        send function
        """
        activateCom()

        if(waitForResponse() == True):
            #response is there, ready to transmit data
            print("True")
        else:
            print("No respones, not transmitting")


async def activateCom():
    GPIO.setmode(GPIO.Board)
    GPIO.setup(27,GPIO.OUT,initial = GPIO.LOW)

    GPIO.output(27,1)
    await asyncio.sleep(1)
    GPIO.output(27,0)

async def waitForResponse():
    GPIO.setmode(GPIO.Board)
    GPIO.setup(27,GPIO.IN)

    channel = GPIO.wait_for_edge(27, GPIO_RISING, timeout = 5000)
    await asyncio.sleep(3)
    if channel is None:
        r = False
        print("Timeout occured")
    else:
        r = True
        print("Edge detected on channel")
    return r
    
        