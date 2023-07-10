# ===============================================================================================
# motion_detection.py
# ===============================================================================================
# Description: Runs on startup and when called. Given the parameters at the top of the file, it
# collects data when motion is detected. Time units in seconds. Does not erase previous folder
# only adds to it. 
#
# Run Command: "python motion_detection.py
# 
# Written By: Guadalupe Bernal 
# Date Last Eddited: 07/06/2023
# ===============================================================================================

import picamera
import picamera.array
import numpy as np
import time
from datetime import datetime
import logging
import shutil
import os

# -----------------------------------------------------------------------------------------------
# General setings
folder_path = '/home/pi/videos'
time_total = 7200
time_motion_record = 10 
time_file_length = 30
camera_cols = 640
camera_rows = 480
framerate = 30
i2c_bus = 10
default_focus = 300
motion_detection = True
# -----------------------------------------------------------------------------------------------
# Motion sensitivity
motion_vectors_norm = 80
motion_density = 100      # number of pixels with |mvecs| > 80
# -----------------------------------------------------------------------------------------------


def init(bus, address):
    os.system("i2cset -y {} 0x{:02x} 0x02 0x00".format(bus, address))

def write(bus, address, value):
    value_high = (value >> 4) & 0x3F
    value_low  = (value << 4) & 0xF0
    os.system("i2cset -y {} 0x{:02x} {} {}".format(bus, address, value_high, value_low))

class Focuser:
    bus = None
    CHIP_I2C_ADDR = 0x0C

    def __init__(self, bus):
        self.focus_value = 0
        self.bus = bus
        self.verbose = False
        init(self.bus, self.CHIP_I2C_ADDR)
        
    def read(self):
        return self.focus_value

    def write(self, chip_addr, value):
        if value < 0:
            value = 0
        self.focus_value = value

        value = int(value)

        write(self.bus, chip_addr, value)

    OPT_BASE    = 0x1000
    OPT_FOCUS   = OPT_BASE | 0x01
    OPT_ZOOM    = OPT_BASE | 0x02
    OPT_MOTOR_X = OPT_BASE | 0x03
    OPT_MOTOR_Y = OPT_BASE | 0x04
    OPT_IRCUT   = OPT_BASE | 0x05
    opts = {
        OPT_FOCUS : {
            "MIN_VALUE": 0,
            "MAX_VALUE": 1000,
            "DEF_VALUE": 0,
        },
    }
    def reset(self,opt,flag = 1):
        info = self.opts[opt]
        if info == None or info["DEF_VALUE"] == None:
            return
        self.set(opt,info["DEF_VALUE"])

    def get(self,opt,flag = 0):
        info = self.opts[opt]
        return self.read()

    def set(self,opt,value,flag = 1):
        info = self.opts[opt]
        if value > info["MAX_VALUE"]:
            value = info["MAX_VALUE"]
        elif value < info["MIN_VALUE"]:
            value = info["MIN_VALUE"]
        self.write(self.CHIP_I2C_ADDR, value)
        if self.verbose:
            print("write: {}".format(value))

# Set up logging
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    
logging.basicConfig(filename=os.path.join(folder_path,'motion.log'), level=logging.INFO, 
                    format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class DetectMotion(picamera.array.PiMotionAnalysis):
    def __init__(self, camera):
        super(DetectMotion, self).__init__(camera)
        self.motion_detected = False
        self.last_detection = time.time()
        self.last_logged = time.time()  # Add this line

    def analyse(self, a):
        a = np.sqrt(
            np.square(a['x'].astype(float)) +
            np.square(a['y'].astype(float))
        ).clip(0, 255).astype(np.uint8)

        
        if (not motion_detection) or ((a > motion_vectors_norm).sum() > motion_density):
            self.motion_detected = True
            self.last_detection = time.time()
            # Only log if at least 1 second has passed since the last log
            if self.last_detection - self.last_logged >= 1:
                logging.info('Motion detected')  # Log the detection
                self.last_logged = self.last_detection  # Update the last logged time

# -----------------------------------------------------------------------------------------------

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

print("Initializing Camera...")
camera = picamera.PiCamera()
print("Camera Initialized")

focuser = Focuser(i2c_bus)
focuser.reset(Focuser.OPT_FOCUS)
print("Initial Focus: ", focuser.get(Focuser.OPT_FOCUS))

focuser.set(Focuser.OPT_FOCUS, int(default_focus))
print("Set Focus: ", focuser.get(Focuser.OPT_FOCUS))

camera.resolution = (camera_cols, camera_rows)
camera.framerate = framerate

print("Start recording...")
output = DetectMotion(camera)
camera.start_recording('/dev/null', format='h264', motion_output=output)

start_time = time.time()

# run the program until time_total 
while time.time() - start_time < time_total:
    camera.wait_recording(0.1)   
    if output.motion_detected:
        
        start_recording_time = time.time()
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = os.path.join(folder_path, timestamp)
        print(f"Motion detected - total time: {int(time.time() - start_time)}  current time: {filename} {int(time.time() - output.last_detection)}")
        
        camera.split_recording(filename)
        output.motion_detected = False
        while (time.time() - output.last_detection) < time_motion_record and (time.time() - start_recording_time) < time_file_length:
            camera.wait_recording(.1)
        # check duration
        dt = int(time.time() - start_recording_time)
        # finish previous recording
        camera.split_recording('/dev/null')
        # rename file with duration
        os.rename(filename, filename + f"_{dt:08d}.h264")
        print(f"Recording File Time = {dt:08d}")        

        output.motion_detected = False
        

print("Stop Recording...")
camera.stop_recording()







