import cv2

# Define the video capture object
cap = cv2.VideoCapture(0)  # Use 0 for the default camera
if cap.isOpened():
    width = 640
    height = 480
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    # Retrieve the capture frame rate
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    print(f"Capture Frame Rate: {frame_rate} fps")
    frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"Capture Resolution: {frame_width}x{frame_height}")    
else:
    print("Failed to retrieve the capture frame rate.")


# Define the video codec and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output = cv2.VideoWriter('output.avi', fourcc, 30.0, (640, 480))  # Adjust the resolution as needed

# fourcc = cv2.VideoWriter_fourcc(*'MP4V')
# output = cv2.VideoWriter('output.mp4', fourcc, 30.0, (640, 480))  # Adjust the resolution as needed



# Set the recording duration
recording_duration = 3  # 20 seconds

# Start the video recording
start_time = cv2.getTickCount()
frames = []
frameCount = 0
while True:
    ret, frame = cap.read()  # Read each frame
    
    # Write the frame to the output video
    # output.write(frame)
    frames.append(frame)
    frameCount += 1

    # Check if the recording duration has been reached
    elapsed_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()    
    if elapsed_time >= recording_duration:
        print(frame.nbytes)
        break

for frame in frames:
    output.write(frame)

print(f"Frame Count = {frameCount}")
# Release the video capture and writer objects
cap.release()
output.release()