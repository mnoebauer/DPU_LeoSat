import time
import serial

ser = serial.Serial(
        port='/dev/ttyAMA0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)
counter=0

mystring = "Hallo"
b = bytes(mystring, 'utf-8')

while 1:
        ser.write(b)
        time.sleep(1)
        counter += 1