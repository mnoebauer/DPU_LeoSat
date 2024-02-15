import qwiic_titan_gps
from time import sleep


print("SparkFun GPS Breakout - XA1110!")
qwiicGPS = qwiic_titan_gps.QwiicTitanGps()


qwiicGPS.begin()
while True:
    if qwiicGPS.get_nmea_data() is True:
        print("Latitude: {}, Longitude: {}, Time: {}".format(
            qwiicGPS.gnss_messages['Latitude'],
            qwiicGPS.gnss_messages['Longitude'],
            qwiicGPS.gnss_messages['Time']))
    sleep(1)