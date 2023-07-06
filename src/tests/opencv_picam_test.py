from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time

# Initialize the camera
camera = PiCamera()

# Set the resolution and framerate
camera.resolution = (640, 480)
camera.framerate = 30

rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.5)

output = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), 30.0, (640, 480))


frameCount = 0
start_time = time.time()
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    if time.time() - start_time >= 10:
        break
    img = frame.array
    output.write(img)
    rawCapture.truncate(0)
    frameCount += 1

print(f"Frame Count = {frameCount}")
output.release()
camera.close()
