# ===============================================================================================
# checkFramerate.py
# ===============================================================================================
# Description: outputs the fps of the video files in a directory
#
# Run Command: "python checkFramerate.py"
#
# Written By: Guadalupe Bernal
# Date Last Eddited: 07/07/2023
# ===============================================================================================


import cv2
import os
from datetime import datetime

# directory containing the videos
video_dir = 'E:/bees/rpi/videos'

# iterate over each file in the video directory
for filename in os.listdir(video_dir):

    if filename.endswith('.h264'):

        # parse duration from filename
        date_string, duration_string = filename.rsplit('_', 1)

        # remove extension
        duration_string = duration_string.replace('.h264', '')
        duration = int(duration_string)

        # open with OpenCV
        video = cv2.VideoCapture(os.path.join(video_dir, filename))
        video = cv2.VideoCapture(os.path.join(video_dir, filename))

        # manually count num of frames in video
        frame_count = 0
        while True:
            ret, frame = video.read()
            if not ret:  # no frame is returned -> reached end of video
                break
            frame_count += 1

        # calculate frame rate
        frame_rate = frame_count / duration

        print(f'Filename: {filename}, Frame Rate: {frame_rate} fps, Frame Count: {frame_count}')

        # release video file
        video.release()

cv2.destroyAllWindows()
