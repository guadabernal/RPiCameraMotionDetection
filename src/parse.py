import cv2

# Load the video
cap = cv2.VideoCapture('E:/bees/rpi/videos/videos/2023-06-23_12-34-49.h264')

# Set initial frame count
frame_count = 0

# Hold current frame
current_frame = None

while cap.isOpened():
    # Read the frame
    ret, frame = cap.read()
    if not ret:
        break

    # Display the frame
    cv2.imshow('Video', frame)
    current_frame = frame.copy()

    # Detect key press
    key = cv2.waitKey(0)

    if key == 83:  # right arrow key
        frame_count += 1
    elif key == 81:  # left arrow key
        frame_count -= 1
        cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, frame_count))
    elif key == 27:  # 'ESC' key
        break

# Release the VideoCapture object
cap.release()
cv2.destroyAllWindows()
