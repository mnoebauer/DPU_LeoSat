import wiringpi
wiringpi.wiringPiSetup()
serial = wiringpi.serialOpen('/dev/ttyAMA0',9600)

while True:
    wiringpi.serialPuts(serial,'hello world!')
