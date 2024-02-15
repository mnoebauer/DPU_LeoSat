import qwiic_titan_gps

class GPS:
    qwiicGPS = qwiic_titan_gps.QwiicTitanGps()
    
    print("gps is conneceted?"+qwiicGPS.begin())

    def read(self):
        if self.qwiicGPS.get_nmea_data() is True:
            lat = self.qwiicGPS.gnss_messages['Latitude']
            long = self.qwiicGPS.gnss_messages['Longitude']
            alt = self.qwiicGPS.gnss_messages['Altitude']
        else:
            print("not true")

        return lat, long, alt
