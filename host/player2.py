import cv2
import os

def play_video(video_path, save_folder):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print("Frames =", total_frames)

    if not cap.isOpened():
        print("Error: Unable to open video file.")
        return

    frame_number = 0  # Initialize the frame number
    increment = 8  # Initialize the frame increment value

    while True:
        # Read a frame from the video
        ret, frame = cap.read()
        frameT = frame.copy()

        if not ret:
            print("End of video.")
            break

        # Add the frame number and increment as text overlay on the frame
        text_overlay = f"Frame: {frame_number}/{total_frames}"
        cv2.putText(frameT, text_overlay, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        text_overlay = f"Inc: {increment}"
        cv2.putText(frameT, text_overlay, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow("Video", frameT)

        # Wait for a key press (0 means wait indefinitely)
        key = cv2.waitKey(0) & 0xFF

        # Press 'q' to quit
        if key == ord('q'):
            break
        elif key == ord('a'):
            frame_number = max(0, frame_number - increment)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        elif key == ord('s'):
            frame_number = max(0, frame_number - 1)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        elif key == ord('d'):
            frame_number = min(total_frames - 1, frame_number + 1)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        elif key == ord('f'):
            frame_number = min(total_frames - 1, frame_number + increment)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        elif key == ord('x'):
            increment = max(1, increment * 2)
        elif key == ord('z'):
            increment = max(1, increment // 2)
        elif key == ord('c'):  # Press 'c' to save the current frame to the specified folder
            filename = os.path.join(save_folder, f"frame_{frame_number:04d}.png")
            cv2.imwrite(filename, frame)
            print(f"Frame {frame_number} saved as {filename}")
            frame_number = min(total_frames - 1, frame_number + 1)
        else:
            frame_number = min(total_frames - 1, frame_number + 1)

    # Release video capture and close the window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = 'E:/bees/BeeMonitoring/DownloadedVideos/01_2023-07-26_10-26-01_00016200.avi'  # Replace with the path to your AVI video file
    save_folder = 'E:/bees/BeeMonitoring/CollectedData'  # Replace with the path to the folder where you want to save frames
    os.makedirs(save_folder, exist_ok=True)
    play_video(video_path, save_folder)
