# DPU-LeoSat Software

Software for the DPU of the Leosat 2024, it includes the Code for gathering Data from the Sensors, taking periodical pictures/videos with the camera and sending the data to the communication PCB.


# Files
flightlogic.py is the main file to be executed while powering on the Raspberry Pi Zero.

getSensorData.py collects all the data and saves it to a CSV file. Furthermore when omething goes wrong it logs it to a text file.

transsmission.py handles the communction between the Radio PCB and the SensorHat. It sends the collected data via UART.

# Usage

First setup Auto-Login into the console in the raspi-config option.
Then add the following line at the bottom of the .bashrc file:

```
python pi/home/DPU_LeoSat/flightLogic.py
```

Now the file is run at the boot of the RPI.