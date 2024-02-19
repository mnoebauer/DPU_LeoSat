from Drivers import HTE501
from time import sleep

hteObj = HTE501.HTE(0x40)

while True:
    temp,hum = hteObj.read()
    print(str(temp)+","+ str(hum))
    sleep(1)
