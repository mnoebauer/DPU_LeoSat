import board
import csv
import asyncio
import RPi.GPIO as GPIO
import serial
import sys
from time import sleep
import codecs

class Transmission:
    """
    Class for transmitting the data to the communication pcb
    """
    async def send():
        """
        Function to send sensor datat to radio pcb via UART
        """
        print("In 10s sleep")
        await asyncio.sleep(10)
        while True:
            print("in while true")
            transmit()
            await asyncio.sleep(3)

def transmit():
    """
        Function that gets the number of the row of the csv file that got sent last time
        increments that und gets the new row. Then establishes the UART connection an sends the data.
        At last the index of the row gets wirtten to the file again.
    """
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(27,GPIO.OUT)
        
        f = open('/home/pi/DPU_LeoSat/data/lastDataSent.txt','r') #opening the systemlog text file in append mode
        oldRow = f.readline()
        f.close()
        
        print(oldRow)
        numOfRow = int(oldRow) + 1
        """
        with open("/home/pi/DPU_LeoSat/data/data.csv", newline= '', encoding ='utf-8') as fd:
            reader = csv.reader(fd)
            rowToSend = [row for idx, row in enumerate(reader) if idx == numOfRow]
        """
        with open("/home/pi/DPU_LeoSat/data/data.csv", newline= '', encoding ='utf-8') as fd:
            reader = csv.reader(fd)
            rowToSend = fd.readlines()[-1]

        ser = serial.Serial(
                port='/dev/ttyAMA0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS, 
                timeout=1
        )

        GPIO.output(27,1)
        #c = ",".join(str(element)for element in rowToSend) #converting list to string
        c = rowToSend
        b = bytes(c, 'utf-8')
        ser.write(b)
        ser.close()
        GPIO.output(27,0)

        f = open('/home/pi/DPU_LeoSat/data/lastDataSent.txt','w') #opening the lastDataSent.txt file in write mode
        f.write(str(numOfRow)) #write the number of the row that got sent to the text file
        f.close()
    except Exception as e: 
        print(e)