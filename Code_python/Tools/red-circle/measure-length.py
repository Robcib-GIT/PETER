"""
    Capture video from the default camera and detect a red circle in the image.
    Jorge F. García-Samartín
    www.gsamartin.es
    2024-05-23
"""

DEBUG = True

import os
from DetectCircles import detect_circles

def main():

    # Get current working directory
    currDir = os.path.dirname(os.path.abspath(__file__)) + "/"

    # Detect the red circles in the video stream
    detected_circles = detect_circles(currDir + "videos/short.mp4")

    # Show the number of detected circles in each frame
    if DEBUG:
        for i, circles in enumerate(detected_circles):
            print(f"Frame {i}: {len(circles)} circles detected")

if __name__ == "__main__":
    main()