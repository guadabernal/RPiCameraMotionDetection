import cv2
import os
from datetime import datetime

# Directory containing the videos
video_dir = 'E:/bees/rpi/videos'
# Iterate over each file in the video directory
for filename in os.listdir(video_dir):
    if filename.endswith('.h264'):
        # Parse the duration from the filename
        date_string, duration_string = filename.rsplit('_', 1)
        duration_string = duration_string.replace('.h264', '')  # Remove the file extension
        duration = int(duration_string)  # Duration in seconds

        # Open the video file with OpenCV
        video = cv2.VideoCapture(os.path.join(video_dir, filename))

        # Open the video file with OpenCV
        video = cv2.VideoCapture(os.path.join(video_dir, filename))

        # Manually count the number of frames in the video
        frame_count = 0
        while True:
            ret, frame = video.read()
            if not ret:  # If no frame is returned, we've reached the end of the video
                break
            frame_count += 1

        # Calculate the frame rate
        frame_rate = frame_count / duration

        print(f'Filename: {filename}, Frame Rate: {frame_rate} fps, Frame Count: {frame_count}')

        # Release the video file
        video.release()

cv2.destroyAllWindows()
