"""
    Function to detect a red circle in a video stream using OpenCV
    Jorge F. García-Samartín
    www.gsamartin.es
    2024-05-31
"""

def detect_circles (video_stream):
    """
    Detects all the red circles in a video stream using OpenCV

    Parameters:
    video_stream: Address of the video stream to process

    Returns:
    circles: Numpy array with the coordiantes of the detected circles.
    """

    # Import the required libraries
    import cv2
    import numpy as np

    # Open the video stream
    cap = cv2.VideoCapture(video_stream)

    # Loop vars
    circles_hist = [];

    # For each frame in the video
    while True:

        # Capture frame-by-frame
        ret, captured_frame = cap.read()

        # If the frame was not captured, break the loop
        if not ret:
            break

        # Convert original image to BGR, since Lab is only available from BGR
        captured_frame_bgr = cv2.cvtColor(captured_frame, cv2.COLOR_BGRA2BGR)
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
            circles_hist.append(circles)
            
