from picamera2 import Picamera2
import time
i = 0

picam2 = Picamera2()
config = picam2.create_still_configuration(main={"size": (1920, 1080)})
picam2.configure(config)
picam2.start()
time.sleep(5)

while 1:

    picam2.capture_file("picture"+ str(i) + ".jpg")
    i += 1
    time.sleep(10)

picam2.stop()