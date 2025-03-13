import cv2
import numpy as np
import glob
import os

# Create a folder to save images with detected corners
output_dir = "detected_corners"
os.makedirs(output_dir, exist_ok=True)

# Checkerboard settings (internal corners)
CHECKERBOARD = (9, 6)  # 9x6 squares = 8x5 corners
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
square_size = 2.5  # Size of one checkerboard square in cm (adjust as needed)

# Prepare 3D object points [(0,0,0), (1,0,0), ..., (7,4,0)]
objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
objp *= square_size  # Scale to real-world size

objpoints = []  # 3D points
imgpoints = []  # 2D points

# Get all calibration images
images = glob.glob("calib_*.jpg")

if not images:
    print("No calibration images found. Make sure your images follow the 'calib_*.jpg' naming pattern.")
    exit()

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find corners
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)
    if ret:
        objpoints.append(objp)
        corners_refined = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners_refined)

        # Draw corners and save the image
        cv2.drawChessboardCorners(img, CHECKERBOARD, corners_refined, ret)
        output_path = os.path.join(output_dir, os.path.basename(fname))
        cv2.imwrite(output_path, img)
        print(f"Saved image with detected corners: {output_path}")

# Check if calibration data was collected
if not objpoints or not imgpoints:
    print("Calibration failed: No corners were detected in any images.")
    exit()

# Perform camera calibration
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None
)

# Save calibration results
np.savez("calibration.npz", mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)

print("\nCamera Matrix:")
print(mtx)
print("\nDistortion Coefficients:")
print(dist)
