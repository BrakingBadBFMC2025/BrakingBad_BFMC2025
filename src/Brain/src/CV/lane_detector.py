import cv2
import numpy as np
import math


def Canny(frame):
    # Converts frame to grayscale because we only need the luminance channel for detecting edges - less computationally expensive
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    # Applies a 5x5 gaussian blur with deviation of 0 to frame - not mandatory since Canny will do this for us
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # Applies Canny edge detector with minVal of 50 and maxVal of 150
    canny = cv2.Canny(blur, 100, 200)
    return canny


def region_selection(image):
    """
    Determine and cut the region of interest in the input image.
    Parameters:
        image: we pass here the output from canny where we have 
        identified edges in the frame
    """
    # create an array of the same size as of the input image 
    mask = np.zeros_like(image)   
    # if you pass an image with more then one channel
    if len(image.shape) > 2:
        channel_count = image.shape[2]
        ignore_mask_color = (255,) * channel_count
    # our image only has one channel so it will go under "else"
    else:
          # color of the mask polygon (white)
        ignore_mask_color = 255
    # creating a polygon to focus only on the road in the picture
    # we have created this polygon in accordance to how the camera was placed
    rows, cols = image.shape[:2]
    bottom_left  = [cols * 0.001, rows * 0.99]
    top_left     = [cols * 0.25, rows * 0.55]
    bottom_right = [cols * 0.999, rows * 0.99]
    top_right    = [cols * 0.75, rows * 0.55]
    vertices = np.array([[bottom_left, top_left, top_right, bottom_right]], dtype=np.int32)
    # filling the polygon with white color and generating the final mask
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    # performing Bitwise AND on the input image and mask to get only the edges on the road
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

def hough_transform(image):
    """
    Determine and cut the region of interest in the input image.
    Parameter:
        image: grayscale image which should be an output from the edge detector
    """
    # Distance resolution of the accumulator in pixels.
    rho = 1             
    # Angle resolution of the accumulator in radians.
    theta = np.pi/180   
    # Only lines that are greater than threshold will be returned.
    threshold = 50      
    # Line segments shorter than that are rejected.
    minLineLength = 50  
    # Maximum allowed gap between points on the same line to link them
    maxLineGap = 50   
    # function returns an array containing dimensions of straight lines 
    # appearing in the input image
    return cv2.HoughLinesP(image, rho = rho, theta = theta, threshold = threshold,
                           minLineLength = minLineLength, maxLineGap = maxLineGap)




def average_slope_intercept(lines):
	"""
	Find the slope and intercept of the left and right lanes of each image.
	Parameters:
		lines: output from Hough Transform
	"""
	left_lines = [] #(slope, intercept)
	left_weights = [] #(length,)
	right_lines = [] #(slope, intercept)
	right_weights = [] #(length,)
	
	for line in lines:
		for x1, y1, x2, y2 in line:
			if x1 == x2:
				continue
			# calculating slope of a line
			slope = (y2 - y1) / (x2 - x1)
			# calculating intercept of a line
			intercept = y1 - (slope * x1)
			# calculating length of a line
			length = np.sqrt(((y2 - y1) ** 2) + ((x2 - x1) ** 2))
			# slope of left lane is negative and for right lane slope is positive
			if  slope < 0:
				left_lines.append((slope, intercept))
				left_weights.append((length))
			elif slope >0:
				right_lines.append((slope, intercept))
				right_weights.append((length))
	# 
	left_lane = np.dot(left_weights, left_lines) / np.sum(left_weights) if len(left_weights) > 0 else None
	right_lane = np.dot(right_weights, right_lines) / np.sum(right_weights) if len(right_weights) > 0 else None
	return left_lane, right_lane

def pixel_points(y1, y2, line):
    """
    Converts the slope and intercept of each line into pixel points.
        Parameters:
            y1: y-value of the line's starting point.
            y2: y-value of the line's end point.
            line: The slope and intercept of the line.
    """
    if line is None:
        return None
    slope, intercept = line

    if slope ==0 or np.isposinf(intercept) or np.isneginf(intercept):
          return None

    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    y1 = int(y1)
    y2 = int(y2)

    return ((x1, y1), (x2, y2))

def trajectory_line(left_line, right_line):
    
    if left_line is None or right_line is None:
        return None

    mean_x1 = int((left_line[0][0] + right_line[0][0])/2)
    mean_x2 = int((left_line[1][0] + right_line[1][0])/2)

    traj_line = {(mean_x1, left_line[0][1]),(mean_x2, left_line[1][1])}

    return traj_line


def lane_lines(image, lines):
	"""
	Create full lenght lines from pixel points.
		Parameters:
			image: The input test image.
			lines: The output lines from Hough Transform.
	"""
	left_lane, right_lane = average_slope_intercept(lines)
	y1 = image.shape[0]
	y2 = y1 * 0.6
	left_line = pixel_points(y1, y2, left_lane)
	right_line = pixel_points(y1, y2, right_lane)
	return left_line, right_line

	

def draw_lane_lines(image, lines, color=[0, 0, 255], thickness=12):
	"""
	Draw lines onto the input image.
		Parameters:
			image: The input test image (video frame in our case).
			lines: The output lines from Hough Transform.
			color (Default = red): Line color.
			thickness (Default = 12): Line thickness. 
	"""
	line_image = np.zeros_like(image)
	for line in lines:
		if line is not None:
			cv2.line(line_image, *line, color, thickness)
	return cv2.addWeighted(image, 1.0, line_image, 1.0, 0.0)

def draw_trajectory_line(image,line, color=[0, 255, 0],thickness=12):
    line_image = np.zeros_like(image)
    if line is not None:
            cv2.line(line_image, *line, color, thickness)
    return cv2.addWeighted(image, 1.0, line_image, 1.0, 0.0)


def filter_weak_lines(lines):
    if lines is None or len(lines) == 0:
        return False
    # Calculate average line length
    lengths = [np.sqrt((x2 - x1)**2 + (y2 - y1)**2) for line in lines for x1, y1, x2, y2 in line]
    avg_length = np.mean(lengths) if lengths else 0
    return avg_length > 50  # Only accept frames with sufficiently strong lines

def get_line_angle(image, line):
    my_list = list(line)
    x1 = my_list[0][0]
    y1 = my_list[0][1]
    x2 = my_list[1][0]
    y2 = my_list[1][1]

    max_y = image.shape[0]
    max_x = image.shape[1]

    slope = ((x1 - x2) / (y1 - y2))
    angle = -math.atan(slope)
    print(angle)
    
    return angle


# Open the default camera (0)
cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cam.read()
    frame_height, frame_width, _ = frame.shape
    if not ret:
        print("Error: Unable to capture video.")
        break

    edges = Canny(frame)
    confined_edges = region_selection(edges)
    hough = hough_transform(confined_edges)
    #cv2.imshow('Webcam', frame)
    #cv2.imshow("edges",confined_edges)
	
    # Check if hough_transform found any lines
    if hough is not None and filter_weak_lines(hough):
        # Generate lane lines
        left_line, right_line = lane_lines(frame, hough)
        traj_line = trajectory_line(left_line, right_line)
        # Draw the lane lines on the frame
        complete_image = draw_lane_lines(frame, [left_line, right_line])
        
        if traj_line is not None:
            get_line_angle(frame,traj_line)
            complete_image = draw_trajectory_line(complete_image, traj_line)
        
        #cv2.imshow("Lane Lines", complete_image)
    else:
        # If no lines are detected, just show the original frame with edges
        #cv2.imshow("Lane Lines", frame)
        pass


    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()