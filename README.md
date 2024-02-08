# DPU-LeoSat Software

Software for the DPU of the Leosat 2024, it includes the Code for gathering Data from the Sensors, taking periodical pictures/videos with the camera and sending the data to the communication PCB.


# Files
flightlogic.py is the main file to be executed while powering on the Raspberry Pi Zero.

hte501_i2c_library.py is the library to use the HTE501 from E+E (https://github.com/epluse/HTE501_i2c_rpi)

# Usage

First setup Auto-Login into the console in the raspi-config option.
Then add the following line at the bottom of the .bashrc file:

python flightLogic.py

Now the file is run at the boot of the RPI.