import wiringpi
wiringpi.wiringPiSetup()
serial = wiringpi.serialOpen('/dev/ttAMA0',baud = 9600)

while True:
    wiringpi.serialPuts(serial,'1')