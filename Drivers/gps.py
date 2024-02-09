import qwiic_titan_gps

class GPS:
    def read():
        qwiicGPS = qwiic_titan_gps.QwiicTitanGps()
        qwiicGPS.begin()
        if qwiicGPS.get_nmea_data() is True:
                lat = qwiicGPS.gnss_messages['Latitude']
                long = qwiicGPS.gnss_messages['Longitude']
                alt = qwiicGPS.gnss_messages['Altitude']

        return lat, long, alt
