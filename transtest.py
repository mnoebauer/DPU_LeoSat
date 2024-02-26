import wiringpi
wiringpi.wiringPiSetup()
serial = wiringpi.serialOpen('/dev/ttyAMA0',115200)

while True:
    wiringpi.serialPuts(serial,'hello world!')