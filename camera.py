from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
import asyncio



class camclass():
        
    picam2 = Picamera2()

    async def takePicture(self):

        f = open('Desktop/DPU_LeoSat/data/picturenumber.txt','r') #opening the bootcycles file in read mode
        i = f.readline()
        f.close()

        config = self.picam2.create_still_configuration(main={"size": (1920, 1080)})
        self.picam2.configure(config)
        self.picam2.start()

        self.picam2.capture_file("picture"+ str(i) + ".jpg")

        i += 1
        
        f = open('Desktop/DPU_LeoSat/data/picturenumber.txt','w') 
        i = f.write(i)
        f.close()
    

    async def takeVideo(self):

        f = open('Desktop/DPU_LeoSat/data/videonumber.txt','r') 
        i = f.readline()
        f.close()

        video_config = self.picam2.create_video_configuration() 
        self.picam2.configure(video_config) 
        
        encoder = H264Encoder(bitrate=10000000) 
        output = "vid" + str(i) +".h264"
        self.picam2.start_recording(encoder, output) 
        await asyncio.sleep(45)
        self.picam2.stop_recording()

        i += 1
        f = open('Desktop/DPU_LeoSat/data/videonumber.txt','w') 
        i = f.write(i)
        f.close()


camclassObj = camclass()

asyncio.run(camclassObj.takePicture()) 