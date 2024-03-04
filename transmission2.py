import board
import csv
import asyncio
import RPi.GPIO as GPIO
import serial
import sys
from time import sleep

class Transmission:
    """
    Class for transmitting the data to the communication pcb
    """
    def send():
        """
        send function
        """
        sleep(10)
        while True:
            activateCom()

            r = waitForResponse()
            
            if r:
                transmit()
            else:
                print("No responnse, not transmitting")
            
            sleep(5)

def activateCom():
    """
    Sending a High Signal to communication pcb to wake up the controller
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(27,GPIO.OUT,initial = GPIO.LOW)

    GPIO.output(27,1)
    sleep(0.1)
    GPIO.output(27,0)

def waitForResponse():
    
    try:
        ser = serial.Serial(
            port='/dev/ttyAMA0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
             baudrate = 9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS, 
            timeout=1
        )
    except:
        print("Serial init failed")

    response  = ser.read()
    decResponse = int.from_bytes(response, byteorder=sys.byteorder) 
    if decResponse == 1:
        return True
    else:
        print("answ failed")
        return False

def transmit():
    """
        Function that gets the number of the row of the csv file that got sent last time
        increments that und gets the new row. Then establishes the UART connection an sends the data.
        At last the index of the row gets wirtten to the file again.
    """

    f = open('/home/pi/data/lastDataSent.txt','r') #opening the systemlog text file in append mode
    oldRow = f.read() #
    f.close()
        
    numOfRow = oldRow + 1

    with open("/home/pi/DPU_LeoSat/data/data.csv") as fd:
        reader = csv.reader(fd)
        rowToSend = [row for idx, row in enumerate(reader) if idx == numOfRow]

    try:
        ser = serial.Serial(
            port='/dev/ttyAMA0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
             baudrate = 9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS, 
            timeout=1
        )
        b = bytes(rowToSend, 'utf-8')
        ser.write(b)
        ser.close()
    except:
        print("com failed")

    f = open('/home/pi/DPU_LeoSat/data/lastDataSent.txt','w') #opening the lastDataSent.txt file in write mode
    f.write(numOfRow) #write the number of the row that got sent to the text file
    f.close()
