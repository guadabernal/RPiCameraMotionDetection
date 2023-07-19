import cv2
import os
from datetime import datetime

# directory containing the videos
video_path = 'E:/bees/videoTemp/2023-07-18_16-26-38_00000120.h264'
cap = cv2.VideoCapture(video_path)
frame_number = 0

total_frames = 0
frames = []
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(frame)
    total_frames += 1
cap.release()

while True:
    frame = frames[frame_number]
    cv2.putText(frame, f'Frame: {frame_number}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('Video Player', frame)
    key = cv2.waitKey(0)
    # Go to the next frame when the 'n' key is pressed
    if key == ord('w'):
        frame_number += 1
        if frame_number == total_frames:
            frame_number = total_frames - 1

    # Go to the previous frame when the 'b' key is pressed
    elif key == ord('s'):
        frame_number -= 1
        if frame_number < 0:
            frame_number = 0

    # Exit the video player when the 'q' key is pressed
    elif key == 27:
        break
cv2.destroyAllWindows()