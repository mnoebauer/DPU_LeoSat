from lib import PiicoDev_MS5637

class ms5637():
    """
    Driver for the MS5637 altitude and pressure sensor, 
    but only the altitude is used
    """
    def read():
        sensor = PiicoDev_MS5637.PiicoDev_MS5637()
        return sensor.read_altitude()
