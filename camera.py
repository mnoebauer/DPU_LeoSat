from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
import asyncio
import time


class camclass():
        
    picam2 = Picamera2()

    async def takePicture(self):

        f = open('/home/pi/DPU_LeoSat/data/picturenumber.txt','r') #opening the bootcycles file in read mode
        i = f.readline()
        f.close()

        config = self.picam2.create_still_configuration(main={"size": (1920, 1080)})
        self.picam2.configure(config)
        self.picam2.start()

        self.picam2.capture_file("picture"+ str(i) + ".jpg")

        i = int(i) + 1
                
        f = open('/home/pi/DPU_LeoSat/data/picturenumber.txt','w') 
        i = f.write(str(i))
        f.close()
        

    async def takeVideo(self):

        f = open('/home/pi/DPU_LeoSat/data/videonumber.txt','r') 
        i = f.readline()
        f.close()

        video_config = self.picam2.create_video_configuration() 
        self.picam2.configure(video_config) 
        
        encoder = H264Encoder(bitrate=1000000) 
        output = "vid" + str(i) +".h264"
        self.picam2.start_recording(encoder, output) 
        asyncio.sleep(45)
        self.picam2.stop_recording()

        i  = int(i) + 1
        f = open('/home/pi/DPU_LeoSat/data/videonumber.txt','w') 
        i = f.write(str(i))
        f.close()
        