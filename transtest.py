import wiringpi
from time import sleep

s = "testtest"

wiringpi.wiringPiSetup()
serial = wiringpi.serialOpen('/dev/ttyAMA0',115200) #115200 Baudrate

while True:
    wiringpi.serialPuts(serial,s) #sends the selected row to com pcb
    print("sent")
    sleep(2)