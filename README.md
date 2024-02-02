# DPU-LeoSat Software

Software for the DPU of the Leosat 2024, it includes the Code for gathering Data from the Sensors and taking periodical pictures with the camera.


# Files
dpu.py is the code to collect, save and transmit the sensor data.

cam.py is the code to take periodical pictures and save them to the storage.

hte501_i2c_library.py is the library to use the HTE501 from E+E (https://github.com/epluse/HTE501_i2c_rpi)

# Usage

First setup Auto-Login into the console in the raspi-config option.
Then add the following line at the bottom of the .bashrc file:

python dpu.py & python cam.py

Now the both files run at the startup.

