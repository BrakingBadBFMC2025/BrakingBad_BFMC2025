import pyrealsense2 as rs

pipeline = rs.pipeline()
pipeline.start()

try:
    for _ in range(10):
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        if depth_frame:
            print("Depth frame captured")
finally:
    pipeline.stop()
