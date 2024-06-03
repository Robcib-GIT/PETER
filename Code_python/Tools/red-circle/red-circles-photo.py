"""
    Capture video from the default camera and detect multipe red circles in the image.
    Jorge F. García-Samartín
    www.gsamartin.es
    2024-05-23
"""

import numpy as np
import cv2
import os

# Get directory of the script
currDir = os.path.dirname(os.path.abspath(__file__)) + "/"

# Capture frame-by-frame
captured_frame = cv2.imread(currDir + "grid.jpg")
output_frame = captured_frame.copy()

# Convert original image to BGR, since Lab is only available from BGR
captured_frame_bgr = cv2.cvtColor(captured_frame, cv2.COLOR_BGRA2BGR)
# First blur to reduce noise prior to color space conversion
captured_frame_bgr = cv2.medianBlur(captured_frame_bgr, 3)
# Convert to Lab color space, we only need to check one channel (a-channel) for red here
captured_frame_lab = cv2.cvtColor(captured_frame_bgr, cv2.COLOR_BGR2Lab)
print(not np.any(captured_frame_lab))
# Threshold the Lab image, keep only the red pixels
# Possible yellow threshold: [20, 110, 170][255, 140, 215]
# Possible blue threshold: [20, 115, 70][255, 145, 120]
captured_frame_lab_red = cv2.inRange(captured_frame_lab, np.array([20, 150, 150]), np.array([190, 255, 255]))
print(not np.any(captured_frame_lab_red))
# Second blur to reduce more noise, easier circle detection
captured_frame_lab_red = cv2.GaussianBlur(captured_frame_lab_red, (5, 5), 2, 2)
print(not np.any(captured_frame_lab_red))
# Use the Hough transform to detect circles in the image
circles = cv2.HoughCircles(captured_frame_lab_red, cv2.HOUGH_GRADIENT, 1, captured_frame_lab_red.shape[0] / 8, param1=100, param2=18, minRadius=5, maxRadius=60)

# Print coordinates of the center of all the detected circles
if circles is not None:
    for circ in circles[0, :]:
        print("Center coordinates: x = {}, y = {}".format(circ[0], circ[1]))
        circles = np.round(circ[0]).astype("int")
        cv2.circle(output_frame, center=(int(circ[0]), int(circ[1])), radius=int(circ[2]), color=(0, 255, 0), thickness=2)

# Display the resulting frame
cv2.imshow('frame', output_frame)
cv2.waitKey(0)

# When everything done, release the capture
cv2.destroyAllWindows()