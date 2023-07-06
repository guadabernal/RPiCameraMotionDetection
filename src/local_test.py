
import cv2

# Set up video capture
video_capture = cv2.VideoCapture(0)  # Use 0 for the default camera
if not video_capture:
    print("Error")
    exit()
print(video_capture)
# Set up motion detection parameters
motion_threshold = 500  # Adjust this value according to your needs
is_motion_detected = False

# Set up video writer
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = None

while True:
    # Read the current frame from the video capture
    ret, frame = video_capture.read()
    print(ret, frame)
    if not ret:
        continue


    # Convert the frame to grayscale for motion detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if is_motion_detected:
        # Continue recording video
        out.write(frame)
    else:
        # Perform motion detection
        if prev_frame is not None:
            frame_diff = cv2.absdiff(prev_frame, gray)
            motion = cv2.countNonZero(frame_diff)
            if motion > motion_threshold:
                is_motion_detected = True
                # Start recording video
                out = cv2.VideoWriter('motion_capture.avi', fourcc, 20.0, (frame.shape[1], frame.shape[0]))

    # Display the frame for visualization
    cv2.imshow('Motion Detection', frame)

    # Check for keypress
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture, video writer, and close the OpenCV window
video_capture.release()
if out is not None:
    out.release()
cv2.destroyAllWindows()