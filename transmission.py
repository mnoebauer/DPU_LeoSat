import board
import csv
import asyncio
import RPi.GPIO as GPIO
import wiringpi

class Transmission:
    """
    Class for transmitting the data to the communication pcb
    """
    async def send():
        """
        send function
        """
        await asyncio.sleep(10)
        while True:
            activateCom()

            if waitForResponse():
                transmit()
            else:
                print("No respones, not transmitting")
            
            await asyncio.sleep(5)


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
    
async def transmit():
    f = open('data/lastDataSent.txt','r') #opening the systemlog text file in append mode
    oldRow = f.read() #
    f.close()
    
    numOfRow = oldRow + 1

    with open("data/data.csv") as fd:
        reader = csv.reader(fd)
        rowToSend = [row for idx, row in enumerate(reader) if idx == numOfRow]
    
    wiringpi.wiringPiSetup()
    serial = wiringpi.serialOpen('/dev/ttyAMA0',9600)
    wiringpi.serialPuts(serial,rowToSend)