import board
import time
import bme680
import adafruit_ds3231

def initRTC():
    global rtc
    i2c = board.I2C()
    rtc = adafruit_ds3231.DS3231(i2c)
    rtc.datetime = time.struct_time((0000,0,0,0,0,0,0,1,-1))

def writeTextToLog(a):
    f = open('data/systemlog.txt','a')
    f.write('\n')
    f.write(str(rtc.datetime.tm_hour)+":"+ str(rtc.datetime.tm_min)+":"+ str(rtc.datetime.tm_sec))
    f.write(a)

def main():
    writeTextToLog('Starting:     Boot')
    initRTC()
    for i in range(10):
        writeTextToLog(1)
         
if __name__ == "__main__":
    main()