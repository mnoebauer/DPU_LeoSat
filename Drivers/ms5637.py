from PiicoDev_MS5637 import PiicoDev_MS5637

class ms5637():

    def read():
        sensor = PiicoDev_MS5637()
        return sensor.read_altitude()
