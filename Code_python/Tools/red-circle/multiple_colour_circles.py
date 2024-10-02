"""
    Read a video or a picture and detect circles of different colours in each frame.
    Jorge F. García-Samartín
    www.gsamartin.es
    2024-09-30
"""

DEBUG = True
SAVE = True
VERBOSE = True

import os
import cv2
import numpy as np
import tqdm
from DetectCircles import *

def read_and_detect():

    # Get current working directory
    currDir = os.path.dirname(os.path.abspath(__file__)) + "/"

    # Load video or image
    file_name = "video3"
    extension = ".mp4"
    video = "C:/Users/jorge/OneDrive - Universidad Politécnica de Madrid/Shares/Doctorado/TFM Ivonne/Video/" + file_name + extension
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
    all_circles = [detect_circles(frame, colors=["blue", "yellow", "green"], num_circles=1) for frame in tqdm.tqdm(frames)]

    # For each row of all_circles, put all the circles in a single list but each frame in a different list
    byg_circles = []
    for circles in all_circles:
        frame_circles = []
        for color_circles in circles:
            frame_circles.extend(color_circles)
        byg_circles.append(frame_circles)

    # Save the results to a csv file with the name of the video
    if SAVE:
        if VERBOSE:
            print(f"Saving results to {currDir}results/{file_name}_heights.csv")
        file_name = os.path.splitext(os.path.basename(video))[0]
        np.savetxt(currDir + "results/" + file_name + "_circles_for_angle.csv", byg_circles, delimiter=";")

def main():
    read_and_detect()

if __name__ == "__main__":
    main()