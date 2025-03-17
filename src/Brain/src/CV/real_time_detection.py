import cv2
import time
from picamera2 import Picamera2
from ultralytics import YOLO

def process_video(output_file="annotated_video.avi", frame_width=640, frame_height=480, fps=12):
    # Initialize Picamera2 with the desired resolution
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (frame_width, frame_height)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    picam2.configure("preview")
    picam2.start()

    # Load the YOLO model (replace with your NCNN model if needed)
    model = YOLO("model_weights/best_ncnn_model/")

    # Setup VideoWriter for saving the annotated video
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    video_writer = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))
    print("Processing video frames. Press Ctrl+C to stop.")

    # For FPS calculation
    start_time = time.time()
    frame_count = 0

    try:
        while True:
            # Capture a frame from the camera
            frame = picam2.capture_array()

            # Run model inference on the frame
            results = model(frame, conf=0.6, imgsz=(frame_width, frame_height))

            # Annotate the frame with detection results
            # (Assumes the YOLO result object provides a .plot() method to draw boxes)
            annotated_frame = results[0].plot()

            # Update FPS calculations
            frame_count += 1
            elapsed_time = time.time() - start_time
            current_fps = frame_count / elapsed_time if elapsed_time > 0 else 0

            # Overlay FPS on the annotated frame
            cv2.putText(annotated_frame, f"FPS: {current_fps:.2f}", (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            # Write the annotated frame to the output video
            video_writer.write(annotated_frame)
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        # Release resources
        video_writer.release()
        picam2.stop()
        cv2.destroyAllWindows()
        print(f"Annotated video saved as {output_file}")

if __name__ == "__main__":
    process_video()
