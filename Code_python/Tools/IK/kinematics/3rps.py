"""
    nverse Kinematics of a 3RPS Robot
    Jorge F. García-Samartín
    www.gsamartin.es
    2024-07-03
"""

import numpy as np

def ik (angles):
    """
    Computes the inverse kinematic model of a 3RPS parallel robot

    Parameters:
    angles (array): Array containing the Euler angles of the central platform.

    Returns:
    l (array): Lengths of the three wires.

    """

    # Defining parameters
    H = 7.5     # Lower triangle height
    h = H       # Upper triangle height
    b = h
    p = 5       # Minimum height
    theta = np.deg2rad(60)

    # Setting the ks
    k1 = b ** 2
    k2 = H ** 2
    k3 = p ** 2
    k4 = -2 * H * p
    k5 = -2 * H * h

    # Getting the lengths
    l = np.empty(3)
    l[0] = np.sqrt(k1 + k2 + k3 + k4*np.sin(angles[1]) + k5*np.cos(angles[1]))
    l[1] = np.sqrt(k1 + k2 + k3 + k4 * (np.cos(angles[1])*np.sin(angles[0])*np.sin(theta) - np.sin(angles[1])*np.cos(theta)) +\
                   k5 * ((np.cos(angles[0]) - np.cos(angles[0])*np.cos(theta)**2 + np.cos(angles[1])*np.cos(theta)**2\
                          + np.sin(angles[0])*np.sin(angles[1])*np.sin(theta)*np.cos(theta))))
    l[2] = np.sqrt(k1 + k2 + k3 - k4 * (np.cos(angles[1])*np.sin(angles[0])*np.sin(theta) + np.sin(angles[1])*np.cos(theta)) +\
                   k5 * ((np.cos(angles[0]) - np.cos(angles[0])*np.cos(theta)**2 + np.cos(angles[1])*np.cos(theta)**2\
                          - np.sin(angles[0])*np.sin(angles[1])*np.sin(theta)*np.cos(theta))))
    
    return l