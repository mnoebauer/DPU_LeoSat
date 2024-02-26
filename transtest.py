import wiringpi
wiringpi.wiringPiSetup()
serial = wiringpi.serialOpen('/dev/serial0,9600')

while True:
    wiringpi.serialPuts(serial,'1')