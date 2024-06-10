"""
    Read a video or a picture and detect a red circle in each frame.
    Jorge F. García-Samartín
    www.gsamartin.es
    2024-05-31
"""

DEBUG = True

import os
import cv2
import numpy as np
from DetectCircles import detect_circles

def main():

    # Get current working directory
    currDir = os.path.dirname(os.path.abspath(__file__)) + "/"

    # Load video or image
    video = currDir + "videos/short.mp4"
    cap = cv2.VideoCapture(video)
    #ret, captured_frame = cap.read()

    # Load all the frames of the video
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)

    # For each frame in the video, map to detected_circles

    # Show the number of detected circles in each frame
    if DEBUG:
        for i, circles in enumerate(detected_circles):
            print(f"Frame {i}: {len(circles)} circles detected")

if __name__ == "__main__":
    main()