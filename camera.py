from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
import asyncio

i = 0

class camclass():
        
    picam2 = Picamera2()
    
    async def takePicture(self):
        config = self.picam2.create_still_configuration(main={"size": (1920, 1080)})
        self.picam2.configure(config)
        self.picam2.start()

        while True:
            self.picam2.capture_file("picture"+ str(i) + ".jpg")
            i += 1
            await asyncio.sleep(10)
    

    async def takeVideo(self):

        video_config = self.picam2.create_video_configuration() 
        self.picam2.configure(video_config) 
        
        encoder = H264Encoder(bitrate=10000000) 
        output = "test.h264" 
        self.picam2.start_recording(encoder, output) 
        await asyncio.sleep(10)
        self.picam2.stop_recording()


camclassObj = camclass()

task = asyncio.create_task(camclassObj.takeVideo())  
while True:
    print("jjd")
