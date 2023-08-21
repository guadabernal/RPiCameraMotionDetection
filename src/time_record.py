# ===============================================================================================
# time_record.py
# ===============================================================================================
# Description: Records a one minute file called video.h264 at the set resolution and framerate
#
# Run Command: "python focus_adjust.py -i 10"
#
# Written By: Guadalupe Bernal
# Date Last Eddited: 07/06/2023
# ===============================================================================================

import time
import picamera

# create an instance of the PiCamera class
print("Camera initialization")
camera = picamera.PiCamera()
print("Camera Created")

# set resolution and frame rate of the camera
camera.resolution = (640, 480)
camera.framerate = 15

# start recording
camera.start_recording('video.h264')
print("Start recording")

# record for one minute
camera.wait_recording(5)
camera.stop_recording()
camera.close()
