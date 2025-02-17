#!/usr/bin/env python
import cv2
import numpy as np

"""
1. Load the video frame.
2. Convert the frame to grayscale.
3. Apply GaussianBlur to the frame.
4. Apply Canny edge detection to the frame.
5. Apply thresholding to the frame.
6. Sliding window approach to detect the lane lines.
    i.   Find the histogram of the image
    ii.  Find the peaks of the histogram
    iii. Divide the image into windows
    iv.  Find the lane lines in each window
7. Fit the lane lines to a polynomial.
8. Draw the lane lines on the image
9. Display the image
"""

resolution = (584, 480) # 480p 16:9 aspect ratio

def show_image(txt, img):
    while True:
        # Show Image using OpenCV.
        cv2.imshow(txt, img)

        # Continue script after 'Esc' has been pressed.
        if cv2.waitKey(0) == 27:
            break



def image_processing_threshold(image):
    # Convert Image to Grayscale.
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian Blur to Grayscale Image.
    blurred_image = cv2.GaussianBlur(grayscale_image, (5, 5), 0)

    # # Find the Edges from the Image using Canny Algorithm.
    # canny_image = cv2.Canny(blurred_image, 50, 150)

    # # Convert Image from Grayscale to Binary.
    _, binary_image = cv2.threshold(blurred_image, 127, 255, cv2.THRESH_BINARY)
    # _, binary_image = cv2.threshold(canny_image, 127, 255, cv2.THRESH_BINARY)

    return binary_image

def roi_tdv(img):
    # Reduce Image Resolution
    frame = cv2.resize(img, (854, 480))

    # Select Coordinates
    tl = (329, 140)
    bl = (275, 284)
    tr = (530, 140)
    br = (589, 284)

    # Apply Geometrical Transformation
    pts1 = np.float32([tl, bl, tr, br])
    pts2 = np.float32([[0, 0], [0, 480], [854, 0], [854, 480]])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    transformed_frame = cv2.warpPerspective(frame, matrix, (854, 480))

    return transformed_frame

def swaaald(img):
    # Convert frame to Grayscale #
    """ Open Image File """
    opencv_image = img
    # """Show image before any processing"""
    # show_image("Image Before Processing...", opencv_image)

    """ Convert Camera Frame from BGR to Lines in Binary """
    binary_image = image_processing_threshold(opencv_image)

    # """ Show image after binary processing """
    # show_image("Image After Binary Procesing...", cv2.resize(binary_image, (853, 480)))

    """ Transform Region-Of-Interest to Top-Down-View """
    frame = roi_tdv(binary_image)
    # show_image("Transformed Frame", frame)

    # Find the starting point of the lanes #
    """ Find the row of pixels in front of the car """
    starting_row = frame[-1, :]
    

    """ Calculate the middle point of this row """
    middle_point = int(starting_row.shape[0] // 2)

    """ Find the x-coordinate where the first pixel is white towards the left side """
    left_side = starting_row[:middle_point]
    leftx_base = middle_point - (np.argmax(left_side[::-1]) + 1)

    """ Find the x-coordinate where the first pixel is white towards the right side """
    right_side = starting_row[middle_point:]
    rightx_base = np.argmax(right_side) + middle_point

    # Use the Sliding Window Algorithm to find both lanes #
    """ Divide Image to 9 Windows """
    windows = 9
    window_height = int(frame.shape[0] // windows)

    """ Identify All Non-Zero Pixels. These pixels identify lane markings """
    nonzero = frame.nonzero()
    nonzeroy = np.array(nonzero[0])  # Y-Coordinates of non zero pixels.
    nonzerox = np.array(nonzero[1])  # X-Coordinates of non zero pixels.

    """ Initialize Parameters Before Loop """
    minpix = 15                         #
    margin = 30                         #
    left_lane_inds = []                 # List of all pixels of the left lane.
    right_lane_inds = []                # List of all pixels of the right lane.
    leftx_current = leftx_base          # Starting point of the left lane.
    rightx_current = rightx_base        # Starting point of the right lane.

    """ Starting Loop """
    for window in range(windows):
        # Calculate Window Boundaries. 
        win_y_low = frame.shape[0] - (window + 1) * window_height
        win_y_high = frame.shape[0] - window * window_height


        # We are moving upwards from the bottom of the image.
        win_xleft_low = leftx_current - margin
        win_xleft_high = leftx_current + margin
        win_xright_low = rightx_current - margin
        win_xright_high = rightx_current + margin


        # Find Left Lane Pixels Inside Current Window.
        good_left_inds = []
        for i in range(len(nonzeroy)):
            if (win_y_low <= nonzeroy[i] < win_y_high) and (win_xleft_low <= nonzerox[i] < win_xleft_high):
                good_left_inds.append(i)

        # Find Right Lane Pixels Inside Current Window.
        good_right_inds = []
        for i in range(len(nonzeroy)):
            if (win_y_low <= nonzeroy[i] < win_y_high) and (win_xright_low <= nonzerox[i] < win_xright_high):
                good_right_inds.append(i)

        # If enough pixels are found, shift the window to their mean position
        if len(good_left_inds) > minpix:
            leftx_current = int(np.mean(nonzerox[good_left_inds]))

        if len(good_right_inds) > minpix:
            rightx_current = int(np.mean(nonzerox[good_right_inds]))

        # Save Founded Pixels.
        if len(good_left_inds) != 0:
            left_lane_inds.append(good_left_inds)

        if len(good_right_inds) != 0:
            right_lane_inds.append(good_right_inds)
            # break

    # Create an output image to draw on
    out_img = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    # Convert list of lane indices to a single array
    left_lane_inds = np.concatenate(left_lane_inds)
    right_lane_inds = np.concatenate(right_lane_inds)

    # Extract left and right lane pixel positions
    leftx = nonzerox[left_lane_inds]
    lefty = nonzeroy[left_lane_inds]
    rightx = nonzerox[right_lane_inds]
    righty = nonzeroy[right_lane_inds]

    # Fit a second-order polynomial (quadratic curve) to each lane line
    left_fit = np.polyfit(lefty, leftx, 2)
    right_fit = np.polyfit(righty, rightx, 2)

    # Generate x and y values for plotting the fitted lanes
    plot_y = np.linspace(0, frame.shape[0] - 1, frame.shape[0])
    left_fit_x = left_fit[0] * plot_y**2 + left_fit[1] * plot_y + left_fit[2]
    right_fit_x = right_fit[0] * plot_y**2 + right_fit[1] * plot_y + right_fit[2]

    # Plot detected lane pixels
    out_img[nonzeroy[left_lane_inds], nonzerox[left_lane_inds]] = [255, 0, 0]  # Left lane in blue
    out_img[nonzeroy[right_lane_inds], nonzerox[right_lane_inds]] = [0, 0, 255]  # Right lane in red

    # Draw the sliding windows
    for window in range(windows):
        # Define window boundaries
        win_y_low = frame.shape[0] - (window + 1) * window_height
        win_y_high = frame.shape[0] - window * window_height
        win_xleft_low = leftx_current - margin
        win_xleft_high = leftx_current + margin
        win_xright_low = rightx_current - margin
        win_xright_high = rightx_current + margin
        
        # Draw the rectangles
        cv2.rectangle(out_img, (win_xleft_low, win_y_low), (win_xleft_high, win_y_high), (0, 255, 0), 2)
        cv2.rectangle(out_img, (win_xright_low, win_y_low), (win_xright_high, win_y_high), (0, 255, 0), 2)

    return out_img
