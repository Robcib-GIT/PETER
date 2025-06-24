"""
    Fatigue test of a single PETER leg
    Jorge F. García-Samartín
    www.gsamartin.es
    2024-07-04
"""

import PETER
import os
import sys
import time
import cv2
import numpy as np

# Get current working directory
curr_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
sys.path.append(curr_dir + 'Tools/red-circle/')
import DetectCircles

def main():

    p = PETER.PETER('COM6')
    cam = cv2.VideoCapture(1)

    # Set the leg to the initial position
    p.write_one_valve_millis(0, 1000)
    time.sleep(3)   
    p.write_one_valve_millis(0, -4000)

    heights = []

    for i in range(10):
        # Move the leg to the position
        p.write_one_valve_millis(0, 1000)
        time.sleep(3)

        # Take a picture
        ret, frame = cam.read()
        cv2.imwrite(curr_dir + 'images/' + str(i) + '-up.png', frame)
        circles = DetectCircles.detect_circles(frame)
        height = DetectCircles.get_mean_height(circles)
        heights.append(height)

        p.write_one_valve_millis(0, -4000)
        time.sleep(6)

        # Take a picture
        ret, frame = cam.read()
        cv2.imwrite(curr_dir + 'images/' + str(i) + '-down.png', frame)
        circles = DetectCircles.detect_circles(frame)
        height = DetectCircles.get_mean_height(circles)
        print(height)

    heights = np.array(heights)
    np.savetxt(curr_dir + 'results/fatigue.csv', heights, delimiter=";")

if __name__ == '__main__':
    main()