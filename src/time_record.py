import time
import picamera

# Create an instance of the PiCamera class
print("Camera initialization")
camera = picamera.PiCamera()
print("Camera Created")

# Set the resolution and frame rate of the camera
camera.resolution = (640, 480)
camera.framerate = 30

# Start recording
camera.start_recording('video.h264')
print("Start recording")
# Record for one minute
camera.wait_recording(60)

# Stop recording
camera.stop_recording()

# Release the camera resources
camera.close()
