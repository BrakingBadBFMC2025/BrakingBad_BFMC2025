import cv2
from picamera2 import Picamera2

def record_video(output_file="records/recorded_video.avi", frame_width=320, frame_height=320, fps=20):
    # Initialize the Picamera2
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (frame_width, frame_height)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    picam2.configure("preview")
    picam2.start()

    # Setup VideoWriter with a codec that works well on the Pi (here we use XVID)
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    video_writer = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

    print("Recording started. Press Ctrl+C to stop.")

    try:
        while True:
            # Capture the frame from the camera
            frame = picam2.capture_array()
            # Write the frame to the video file
            video_writer.write(frame)
    except KeyboardInterrupt:
        print("\nRecording stopped by user.")
    finally:
        # Release resources
        video_writer.release()
        picam2.stop()
        cv2.destroyAllWindows()
        print(f"Video saved as {output_file}")

if __name__ == "__main__":
    record_video()
