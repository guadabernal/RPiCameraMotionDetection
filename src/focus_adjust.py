# ===============================================================================================
# focus_adjust.py
# ===============================================================================================
# Description: Runs over range of focus values storing results in folder called "focus" in the 
# directory program was run on RPiW0 with the Arducam Motorized Focus Pi Camera OV5647 5MP 1080P
# Erases previous folder.
#
# Run Command: "python focus_adjust.py -i 10"
# 
# Written By: Guadalupe Bernal 
# Date Last Eddited: 07/06/2023
# ===============================================================================================

import sys
import time
import os
import picamera
import argparse
import shutil

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


def parse_cmdline():
    parser = argparse.ArgumentParser(description='Arducam Controller.')
    parser.add_argument('-i', '--i2c-bus', type=int, nargs=None, required=True,
                        help='Set i2c bus. For arducam + raspberry pi zero W use -i 10')
    return parser.parse_args()



# -----------------------------------------------------------------------------------------------

args = parse_cmdline()
 
# Create an instance of the PiCamera class
print("Camera initialization")
camera = picamera.PiCamera()
print("Camera Created")

focuser = Focuser(args.i2c_bus)
focuser.reset(Focuser.OPT_FOCUS)
print("Focus: ", focuser.get(Focuser.OPT_FOCUS))

# set resolution and framerate
camera.resolution = (640, 480)
camera.framerate = 30

folder_path = '/home/pi/focus'
if os.path.exists(folder_path):
    shutil.rmtree(folder_path)
    print(f"Folder '{folder_path}' and its contents have been deleted.")
os.makedirs(folder_path)

start_focus = 250
end_focus = 350
step_size = 10

# iterate through different focus values for 5 seconds each
# and store each in a file
for focus in range(start_focus, end_focus, step_size):
    
    focuser.set(Focuser.OPT_FOCUS, int(focus))
    print("Focus: ", focuser.get(Focuser.OPT_FOCUS))
    
    filename = os.path.join(folder_path,f'video_{focus:04d}.h264')
    camera.start_recording(filename)
    print(f"Start recording ... {filename}")
    
    # record for 5 seconds
    camera.wait_recording(5)
    camera.stop_recording()

# release the camera resources
camera.close()


