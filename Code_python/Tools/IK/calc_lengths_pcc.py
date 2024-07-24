"""
    Calculate lengths using PCC
    Jorge F. García-Samartín
    www.gsamartin.es
    2024-07-02
"""
# Import libraries
import numpy as np
import os
import kinematics

from scipy.spatial.transform import Rotation

def quat2eul (quat):
    """
    Convert a quaternion to Euler angles

    Parameters:
    quat (array): Quaternion in the form [x, y, z, w]

    Returns:
    eul (array): Euler angles in the form [roll, pitch, yaw]

    """
    eul = np.zeros(3)

    eul[0] = np.arctan2(2* (quat[0] * quat[1] + quat[2] * quat[3]), quat[0] ** 2 - quat[1] ** 2 - quat[2] ** 2 + quat[3] ** 2)
    eul[1] = np.arcsin(-2 * (quat[0] * quat[2] - quat[3] * quat[1]) / (quat[0] ** 2 + quat[1] ** 2 + quat[2] ** 2 + quat[3] ** 2))
    eul[2] = np.arctan2(2 * (quat[1] * quat[2] + quat[0] * quat[3]), -quat[0] ** 2 - quat[1] ** 2 + quat[2] ** 2 + quat[3] ** 2)

    return eul

def main ():
    # Get current working directory
    curr_dir = os.path.dirname(os.path.abspath(__file__)) + "/"

    # Read CSV file containing inflation times and orientations
    csv_values = np.genfromtxt(curr_dir + 'positions1_data.csv', delimiter=',')
    times = csv_values[1:,:3]
    orientations = csv_values[1:,3:]

    # Convert the orientations to Rotation matrices
    R = Rotation.from_euler('ZYX', orientations[0,:], degrees=True).as_matrix()

    # Getting parameters
    phi = np.arctan2(R[2,1], R[2,0])
    c = R[2,2]
    s = R[2,1] / np.sin(phi)
    print('phi:', phi)
    print(np.arccos(c), np.arcsin(s))

    print('The end')

if __name__ == '__main__':
    main()