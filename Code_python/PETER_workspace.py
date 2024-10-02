"""
    Calculate PETER's workspace

    Jorge F. García-Samartín
    wwww.gsamartin.es
    2024-09-30
"""

import numpy as np
import tqdm
import matplotlib.pyplot as plt
from  PETER_IK_TRF import calculate_effector_position
num_modules = 1

def main():

    # Define the workspace limits
    t_min = np.array([0, 0, 0])
    t_max = np.array([2000, 2000, 2000])
    step = 100

    # Calculate the workspace
    pos_all = []
    for t0 in tqdm.tqdm(range(t_min[0], t_max[0], step)):
        for t1 in range(t_min[1], t_max[1], step):
            for t2 in range(t_min[2], t_max[2], step):
                valves = np.array([[t0, t1, t2]])
                pos = calculate_effector_position(valves)

                pos_all.append(pos)

    pos_all = np.array(pos_all)

    # Plot the workspace
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(pos_all[:, 0], pos_all[:, 1], pos_all[:, 2])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()
    plt.waitforbuttonpress
    

if __name__ == "__main__":
    main()