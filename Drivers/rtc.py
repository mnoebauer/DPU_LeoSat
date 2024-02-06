import adafruit_ds3231
import board

class RTC:
    """
    Driver for the DS3231 RTC Module to get the time
    """
    def read():
        i2c = board.I2C()
        rtc = adafruit_ds3231(i2c)

        r = rtc.datetime
        t = str(r.tm_hour) +":"+ str(r.tm_min)+":"+ str(r.tm_sec)
        return t

    def set():
        i2c = board.I2C()  
        rtc = adafruit_ds3231.DS3231(i2c)   
        rtc.datetime = time.struct_time((2024,0,0,0,0,0,0,1,-1)) #setting the hours to 0 to get the start time