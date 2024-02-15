import qwiic_titan_gps

qwiicGPS = qwiic_titan_gps.QwiicTitanGps()
qwiicGPS.begin()

while True:
    if qwiicGPS.get_nmea_data() is True:
        lat = qwiicGPS.gnss_messages['Latitude']
        long = qwiicGPS.gnss_messages['Longitude']
        alt = qwiicGPS.gnss_messages['Altitude']
    else:
        print("not true")
        lat = "NaN"
        long = "NaN"
        alt = "NaN"
            
    print(str(lat,long,alt))
