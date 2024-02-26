'''import wiringpi
wiringpi.wiringPiSetup()
serial = wiringpi.serialOpen('/dev/ttyAMA0',115200)

while True:
    wiringpi.serialPuts(serial,'hello world!')
'''

import serial
from time import sleep
while True:
    ser = serial.Serial ("/dev/ttyAMA0")    #Open named port 
    ser.baudrate = 115200                     #Set baud rate to 9600
    data = "Test"                    #Read ten characters from serial port to data
    ser.write(data)                         #Send back the received data
    ser.close()        
    sleep(1)