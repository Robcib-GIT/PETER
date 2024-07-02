"""
    Function to detect a red circle in an imageusing OpenCV
    Jorge F. García-Samartín
    www.gsamartin.es
    2024-05-31
"""

def detect_circles (image):
    """
    Detects all the red circles in an image using OpenCV

    Parameters:
    image: numpy array containing the image to process

    Returns:
    circles: Numpy array with the coordiantes of the detected circles.
    """

    # Import the required libraries
    import numpy as np
    import cv2

    # Convert original image to BGR, since Lab is only available from BGR
    captured_frame_bgr = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    # First blur to reduce noise prior to color space conversion
    captured_frame_bgr = cv2.medianBlur(captured_frame_bgr, 3)
    # Convert to Lab color space, we only need to check one channel (a-channel) for red here
    captured_frame_lab = cv2.cvtColor(captured_frame_bgr, cv2.COLOR_BGR2Lab)

    # Threshold the Lab image, keep only the red pixels
    # Possible yellow threshold: [20, 110, 170][255, 140, 215]
    # Possible blue threshold: [20, 115, 70][255, 145, 120]
    captured_frame_lab_red = cv2.inRange(captured_frame_lab, np.array([20, 150, 150]), np.array([190, 255, 255]))

    # Second blur to reduce more noise, easier circle detection
    captured_frame_lab_red = cv2.GaussianBlur(captured_frame_lab_red, (5, 5), 2, 2)

    # Use the Hough transform to detect circles in the image
    circles = cv2.HoughCircles(captured_frame_lab_red, cv2.HOUGH_GRADIENT, 1, captured_frame_lab_red.shape[0] / 8, param1=100, param2=18, minRadius=5, maxRadius=60)

    # Save the coordinates of all the detected circles
    if circles is not None:
        return circles[0]
    else:
        return [[-1, -1, -1]]
            
def get_mean_height(circles): 
    """
    Calculate the mean height of the detected circles in the image

    Parameters:
    circles: Numpy array with the coordiantes of the detected circles.

    Returns:
    mean_height: Mean height of the fist two detected circles.
    """

    # Import the required libraries
    import numpy as np

    # If there are less than two circles detected, return -1
    if len(circles) < 2:
        return -1

    # Calculate the mean height
    mean_height = np.mean([circles[0][1], circles[1][1]])

    return mean_height

def filter_data(mean_heights):
    """
    Filter the mean heights of the platform in each frame

    Parameters:
    mean_heights: List with the mean heights of the platform in each frame

    Returns:
    filtered_heights: List with the filtered mean heights of the platform in each frame
    """

    # Import the required libraries
    import numpy as np

    # Filter the data
    filtered_heights = []
    for i in range(0, len(mean_heights) - 1):

        if i == 604:
            print('Hi')

        # Deleting the -1 values
        if mean_heights[i] == -1:
            # Make the mean of the previous and the first value different from -1
            for j in range(i, len(mean_heights) - 1):
                if mean_heights[j] != -1:
                    filtered_heights.append(np.mean([mean_heights[j], filtered_heights[i - 2]]))
                    break

        # Deleting the values that are too different from the two previous ones
        elif i > 1 and\
            abs(mean_heights[i] - filtered_heights[i - 1]) > 0.05*filtered_heights[i - 1] and \
            abs(mean_heights[i] - filtered_heights[i - 2]) > 0.05*filtered_heights[i - 2]:
            filtered_heights.append(np.mean([filtered_heights[i - 1], filtered_heights[i - 2]]))

        else:
            filtered_heights.append(mean_heights[i])

    return filtered_heights