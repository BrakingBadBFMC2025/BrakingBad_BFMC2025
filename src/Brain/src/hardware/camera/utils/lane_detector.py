import cv2
import numpy as np

def processingThreshold(img:cv2.Mat, res:tuple) -> cv2.Mat:
    size = (5, 5)

    # /\/\/\/\/\ Resize Image if Needed /\/\/\/\/\/\
    image = cv2.resize(img, res)

    # Convert Image to Grayscale.
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur to (...)
    image = cv2.GaussianBlur(image, size, 0)

    # Apply Canny Edge Detector.
    image = cv2.Canny(image, 50, 150)

    return image

def regionOfInterest(image:cv2.Mat, res:tuple) -> cv2.Mat:
    height = res[1]
    width = res[0]
    
    tl = (187  , 300)
    bl = (0    , height)
    tr = (463  , 300)
    br = (width, height)

    # apply geometrical tranformation
    roi = np.float32([tl, bl, tr, br])
    points = np.float32([[0, 0], [0, res[1]], [res[0], 0], [res[0], res[1]]])
    perspective = cv2.getPerspectiveTransform(roi, points)
    new_frame = cv2.warpPerspective(image, perspective, res)

    # Transform Image to Binary.
    _, image = cv2.threshold(new_frame, 127, 255, cv2.THRESH_BINARY)

    return image

def startingPositions(img:cv2.Mat, res:tuple) -> tuple:
    # img.shape = (480, 640)

    # Calculating Middle Index.
    middlePoint = int(res[1] // 2)

    # Prepare Areas of Search for Each Line.
    lastRow = img[res[1] - 1, :]
    leftHalf = lastRow[ :middlePoint]
    leftHalfFlipped = np.flip(leftHalf)
    rightHalf = lastRow[middlePoint: ]

    # Left Starting Index
    lP = np.abs(np.argmax(leftHalfFlipped) - middlePoint) - 1
    if lP == middlePoint - 1:
        lP = None

    # Right Starting Point.
    rP = np.argmax(rightHalf) + middlePoint
    if rP == middlePoint:
        rP == None

    return lP, rP

def getLane(nonZeroX:tuple, nonZeroY:tuple, laneInds:list) -> np.ndarray:
    xPixels = nonZeroX[laneInds]
    yPixels = nonZeroY[laneInds]
    lane = np.polyfit(yPixels, xPixels, 2)

    return lane

def slidingWindowAlgorithm(warped:cv2.Mat, res:tuple, lp:int, rp:int) -> int:
    # img.shape = (480, 640)
    leftx_base = lp
    rightx_base = rp

    # Define Parameters.
    nwindows = 9
    margin = 30
    minpix = 10
    window_height = int(warped.shape[0] // nwindows)

    # Identify lane pixels.
    left_lane_inds = []
    right_lane_inds = []
    nonzero = warped.nonzero()
    if len(nonzero) == 0:
        return 0

    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])

    for window in range(nwindows):
        # Define window boundaries.
        win_y_low = warped.shape[0] - (window + 1) * window_height
        win_y_high = warped.shape[0] - window * window_height

        # Identify nonzero pixels in the window.
        good_left_inds = []
        if lp != None:
            win_xleft_low = leftx_base - margin
            win_xleft_high = leftx_base + margin
            for i in range(len(nonzeroy)):
                if (win_y_low <= nonzeroy[i] < win_y_high) and (win_xleft_low <= nonzerox[i] < win_xleft_high):
                    good_left_inds.append(i)

        # Find Right Lane Pixels Inside Current Window.
        good_right_inds = []
        if rp != None:
            win_xright_low = rightx_base - margin
            win_xright_high = rightx_base + margin
            for i in range(len(nonzeroy)):
                if (win_y_low <= nonzeroy[i] < win_y_high) and (win_xright_low <= nonzerox[i] < win_xright_high):
                    good_right_inds.append(i)

        # Append indices to the lists
        left_lane_inds.append(good_left_inds)
        right_lane_inds.append(good_right_inds)

        # Recenter the window if enough pixels are found
        if len(good_left_inds) > minpix:
            leftx_base = int(np.mean(nonzerox[good_left_inds]))
        elif len(good_right_inds) > minpix:
            rightx_base = int(np.mean(nonzerox[good_right_inds]))

    # Concatenate the arrays of indices
    left_lane_inds = np.concatenate(left_lane_inds)
    right_lane_inds = np.concatenate(right_lane_inds)

    # Casting array elements from numpy.floa64 -> numpy.int64
    left_lane_inds = np.array(left_lane_inds, dtype=np.int64)
    right_lane_inds = np.array(right_lane_inds, dtype=np.int64)

    # Number of pixels detected
    left_n = len(left_lane_inds)
    right_n = len(right_lane_inds)

    out_img = np.dstack((warped, warped, warped)) * 255
    out_img = out_img.astype(np.uint8)

    # Check if both lanes have been detected.
    if left_n > 0 and right_n > 0:
        print('\t\t'+ '**Both** lanes have been detected...')
        # Re-construct lanes.
        leftPolyfit = getLane(nonzerox, nonzeroy, left_lane_inds)
        rightPolyfit = getLane(nonzerox, nonzeroy, right_lane_inds)

        # Generate x and y values for plotting
        ploty = np.linspace(0, warped.shape[0] - 1, warped.shape[0])
        left_fitx = leftPolyfit[0] * ploty**2 + leftPolyfit[1] * ploty + leftPolyfit[2]
        right_fitx = rightPolyfit[0] * ploty**2 + rightPolyfit[1] * ploty + rightPolyfit[2]

        lane_center = int(left_fitx[-1] + right_fitx[-1]) / 2
        vehicle_center = int(warped.shape[1] / 2)
        offset = lane_center - vehicle_center

        # Color the lane pixels: note that OpenCV uses BGR format
        out_img[nonzeroy[left_lane_inds], nonzerox[left_lane_inds]] = [0, 0, 255]   # Red for left lane
        out_img[nonzeroy[right_lane_inds], nonzerox[right_lane_inds]] = [255, 0, 0]  # Blue for right lane

        # Create polyline points for left and right lane lines
        pts_left = np.array([[int(x), int(y)] for x, y in zip(left_fitx, ploty)], dtype=np.int64)
        pts_left = pts_left.reshape((-1, 1, 2))
        pts_right = np.array([[int(x), int(y)] for x, y in zip(right_fitx, ploty)], dtype=np.int64)
        pts_right = pts_right.reshape((-1, 1, 2))

        # Draw the lane lines using cv2.polylines
        # For yellow in BGR, use (0, 255, 255)
        cv2.polylines(out_img, [pts_left], isClosed=False, color=(0, 255, 255), thickness=2)
        cv2.polylines(out_img, [pts_right], isClosed=False, color=(0, 255, 255), thickness=2)

    elif left_n == 0 and right_n > 0:
        print('\t\t'+ 'Only **RIGHT** lane has been detected')
        offset = 0

    elif left_n > 0 and right_n == 0:
        print('\t\t'+ 'Only **LEFT** lane has been detected')
        offset = 0

    else:
        print('\t\t'+ '**NONE** lane has been detected')
        offset = 0

    return int(offset), out_img

def lane_detector(image):
    resolution = (640, 480)
    frame = processingThreshold(image, resolution)

    # Add Region of Interest to Image.
    frame = regionOfInterest(frame, resolution)

    # Find the Starting Position of Each Line.
    leftPoint, rightPoint = startingPositions(frame, resolution)

    # Execute Sliding Window Algorithm.
    turn, cameraFrame = slidingWindowAlgorithm(frame, resolution, leftPoint, rightPoint)

    # Decision making.
    if np.abs(turn) < 30:
        string = 'We will go **STRAIGHT**!'
    elif turn > 30:
        string = 'Turning **RIGHT**'
    else:
        string = 'Turning **LEFT**'

    print('\t' + f'Offset is {turn}.' + ' ' + string)

    return turn, cameraFrame