"""
    Read a video or a picture and detect a red circle in each frame.
    Jorge F. García-Samartín
    www.gsamartin.es
    2024-05-31
"""

DEBUG = True
SAVE = True
VERBOSE = True

import os
import cv2
import numpy as np
from DetectCircles import *

def complete_with_filter():

    # Get current working directory
    currDir = os.path.dirname(os.path.abspath(__file__)) + "/"

    # Load video or image
    file_name = "time_length"
    extension = ".mp4"
    video = "D:/Tesis/PETER/Bike/" + file_name + extension
    cap = cv2.VideoCapture(video)

    # Load all the frames of the video
    if VERBOSE:
        print(f"Loading video: {video}")
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)

    # For each frame in frames, map to detected_circles
    if VERBOSE:
        print(f"Processing {len(frames)} frames to detect circles")
    detected_circles = list(map(detect_circles, frames))

    # Show the number of detected circles in each frame
    if DEBUG:
        for i, circles in enumerate(detected_circles):
            print(f"Frame {i}: {len(circles)} circles detected")

    # For each frame, calculate mean height of the first two detected circles (of the platform)
    if VERBOSE:
        print(f"Calculating mean height of the platform in each frame")
    mean_heights = list(map(get_mean_height, detected_circles))
    if DEBUG:
        print(mean_heights)

    # Save the results to a csv file with the name of the video
    if SAVE:
        file_name = os.path.splitext(os.path.basename(video))[0]
        np.savetxt(currDir + "results/" + file_name + "_heights.csv", mean_heights, delimiter=";")

    # Filter the data
    if VERBOSE:
        print(f"Filtering the data")
    filtered_heights = filter_data(mean_heights)
    if DEBUG:
        print(filtered_heights)
    if SAVE:
        np.savetxt(currDir + "results/" + file_name + "_heights_filtered.csv", filtered_heights, delimiter=";")

def only_filter():
    # Setup
    currDir = os.path.dirname(os.path.abspath(__file__)) + "/"
    file_name = "TwoSteps"

    # Load data
    mean_heights = np.loadtxt(currDir + "results/" + file_name + "_heights.csv", delimiter=";")

    # Filter the data
    if VERBOSE:
        print(f"Filtering the data")
    filtered_heights = filter_data(mean_heights)
    if DEBUG:
        print(filtered_heights)
    if SAVE:
        np.savetxt(currDir + "results/" + file_name + "_heights_filtered.csv", filtered_heights, delimiter=";")

if __name__ == "__main__":
    complete_with_filter()