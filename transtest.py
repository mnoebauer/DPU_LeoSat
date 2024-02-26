'''import wiringpi
wiringpi.wiringPiSetup()
serial = wiringpi.serialOpen('/dev/ttyAMA0',9600)

while True:
    wiringpi.serialPuts(serial,'hello world!')
'''
#!/usr/bin/env python
import time
import serial

ser = serial.Serial(
        port='dev/serial0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

while 1:
        x=ser.readline()
        print (x)