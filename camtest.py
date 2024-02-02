from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
import time
i = 0

class camclass():
    
    def takePicture():
        picam2 = Picamera2()
        config = picam2.create_still_configuration(main={"size": (1920, 1080)})
        picam2.configure(config)
        picam2.start()
        picam2.capture_file("picture"+ str(i) + ".jpg")
        i += 1
    
    def takeVideo():
        picam2 = Picamera2()
        video_config = picam2.create_video_configuration() 
        picam2.configure(video_config) 
        
        encoder = H264Encoder(bitrate=10000000) 
        output = "test.h264" 
        picam2.start_recording(encoder, output) 
        time.sleep(10) 
        picam2.stop_recording()