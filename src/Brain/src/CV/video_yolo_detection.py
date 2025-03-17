#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import cv2
import time
import argparse
from ultralytics import YOLO

def process_video(input_video, output_video, model_path="model_weights/best.pt", conf_threshold=0.5):
    print(input_video, output_video, model_path, conf_threshold)
    # 1. Load the YOLO model
    model = YOLO(model_path)

    # 2. Open the input video file
    cap = cv2.VideoCapture(input_video)
    if not cap.isOpened():
        print(f"Error: Could not open input video {input_video}")
        return

    # 3. Retrieve video properties for the output video writer
    width  = 640
    height = 480
    fps    = cap.get(cv2.CAP_PROP_FPS)

    # Use a codec such as mp4v or XVID (adjust if necessary)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    frame_count = 0
    total_inference_time = 0.0

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # End of video

        # 4. Run YOLO detection on the frame
        start = time.time()
        results = model(frame, conf=conf_threshold, imgsz=(width,height))
        inference_time = time.time() - start
        total_inference_time += inference_time
        frame_count += 1

        # Since the model returns a list (one per image), we take the first element
        result = results[0]

        # 5. Draw bounding boxes and labels (if detections exist)
        if result.boxes is not None:
            for box in result.boxes:
                # Extract coordinates, confidence, and class id
                x1, y1, x2, y2 = box.xyxy[0]
                conf = float(box.conf[0])
                cls_id = int(box.cls[0])
                label = model.names[cls_id] if model.names else str(cls_id)

                # Convert coordinates to integer
                x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

                # Draw the rectangle and label on the frame
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # 6. Write the processed frame to the output video file
        out.write(frame)

    # Clean up resources
    cap.release()
    out.release()

    avg_fps = frame_count / total_inference_time if total_inference_time > 0 else 0
    print(f"Processed {frame_count} frames in {total_inference_time:.2f} seconds (avg FPS: {avg_fps:.2f})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run YOLO detection on a video and save the output.")
    parser.add_argument("input_video", help="Path to the input video file.")
    parser.add_argument("output_video", help="Path where the output video will be saved.")
    parser.add_argument("--model", default="model_weights/best.pt", help="Path to the YOLO model file (default: best.pt).")
    parser.add_argument("--conf", type=float, default=0.5, help="Confidence threshold for detections (default: 0.5).")
    args = parser.parse_args()

    process_video(args.input_video, args.output_video, args.model, args.conf)
