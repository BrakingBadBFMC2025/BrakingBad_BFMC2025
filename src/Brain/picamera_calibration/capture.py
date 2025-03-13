from picamera2 import Picamera2
import time
import cv2

picam2 = Picamera2()
config = picam2.create_still_configuration(main={"size": (640, 480)})
picam2.configure(config)
picam2.start()
time.sleep(2)  # Warm-up

for i in range(20):  # Capture 20 images
    image = picam2.capture_array("main")
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(f'calib_{i:02d}.jpg', image)
    print(f"Saved calib_{i:02d}.jpg")
    time.sleep(5)  # Move the checkerboard now!

picam2.stop()