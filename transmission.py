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
    """
    Sending a High Signal to communication pcb to wake up the controller
    """
    GPIO.setmode(GPIO.Board)
    GPIO.setup(27,GPIO.OUT,initial = GPIO.LOW)

    GPIO.output(27,1)
    await asyncio.sleep(0.1)
    GPIO.output(27,0)

async def waitForResponse():
    """
    Setting pin to input and waiting 1 second for an acknowledge from the communication pcb.
    If acknowledge came within that time, the variable gets set true, if not the on false.
    """
    GPIO.setmode(GPIO.Board)
    GPIO.setup(27,GPIO.IN)

    channel = GPIO.wait_for_edge(27, GPIO_RISING, timeout = 1000)
    if channel is None:
        r = False
    else:
        r = True
    return r
    
async def transmit():
    """
    Function that gets the number of the row of the csv file that got sent last time
    increments that und gets the new row. Then establishes the UART connection an sends the data.
    At last the index of the row gets wirtten to the file again.
    """

    f = open('data/lastDataSent.txt','r') #opening the systemlog text file in append mode
    oldRow = f.read() #
    f.close()
    
    numOfRow = oldRow + 1

    with open("data/data.csv") as fd:
        reader = csv.reader(fd)
        rowToSend = [row for idx, row in enumerate(reader) if idx == numOfRow]
    
    wiringpi.wiringPiSetup()
    serial = wiringpi.serialOpen('/dev/ttyAMA0',115200) #115200 Baudrate
    wiringpi.serialPuts(serial,rowToSend) #sends the selected row to com pcb

    f = open('data/lastDataSent.txt','w') #opening the lastDataSent.txt file in write mode
    f.write(numOfRow) #write the number of the row that got sent to the text file
    f.close()