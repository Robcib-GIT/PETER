"""
    Forward and Inverse Kinematics using PCC
    Jorge F. García-Samartín
    www.gsamartin.es
    2024-07-01
"""

import numpy as np

##########################################
#  Forward Kinematics
##########################################
def fk_dependent (l, a = 45):
    """
    Forward Kinematics for a PCC robot segment - Dependent Modelling

    Parameters:
    l (list or array): Lengths of the cables (should be a vector of three lengths).
    a (float): Diameter (in mm) of the circumference formed by the cables.

    Returns:
    params (dict): Dictionary containing 'lr' (mean length), 'phi' (orientation), and 'kappa' (curvature).
    
    """
    # Initial checks
    if len(l) != 3:
        raise ValueError("Provide a vector of three lengths")
    
    # General case
    if not all(el == l[0] for el in l):
        lr = np.mean(l)
        phi = np.arctan2(np.sqrt(3) * (-2*l[0] + l[1] + l[2]), 3 * (l[1] - l[2]))
        kappa = 2 * np.sqrt(l[0]**2 + l[1]**2 + l[2]**2 - l[0]*l[1] - l[2]*l[1] - l[0]*l[2]) / a / (l[0] + l[1] + l[2])

    # Singular position
    else:
        lr = l[0]
        phi = 0
        kappa = 0

    params = {'lr': lr, 'phi': phi, 'kappa': kappa}
    return params

def fk_independent (params):
    """
    Forward Kinematics for a PCC robot segment - Independet Modelling

    Parameters:
    params (dict): Dictionary containing 'lr' (mean length), 'phi' (orientation), and 'kappa' (curvature).

    Returns:
    T (array): Homogeneous transformation matrix.

    """

    # General case
    if params['phi'] and params['kappa']:
        Trot = np.array([[np.cos(params['phi']), -np.sin(params['phi']), 0, 0],
                        [np.sin(params['phi']),  np.cos(params['phi']), 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])
        Tarc = np.array([[np.cos(params['kappa']*params['lr']), 0, np.sin(params['kappa']*params['lr']), (1-np.cos(params['kappa']*params['lr']))/params['kappa']],
                        [0, 1, 0, 0],
                        [-np.sin(params['kappa']*params['lr']), 0, np.cos(params['kappa']*params['lr']), np.sin(params['kappa']*params['lr'])/params['kappa']],
                        [0, 0, 0, 1]])
        T = np.dot(Trot, Tarc)

    # Singular position
    else:
        T = np.array([[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, params['lr']],
                    [0, 0, 0, 1]])
        
    return T
    
def fk (l, a = 45):
    """
    Forward Kinematics for a PCC robot segment

    Parameters:
    l (list or array): Lengths of the cables (should be a vector of three lengths).
    a (float): Diameter (in mm) of the circumference formed by the cables.

    Returns:
    T (array): Homogeneous transformation matrix.
    params (dict): Dictionary containing 'lr' (mean length), 'phi' (orientation), and 'kappa' (curvature).
    
    """

    # Initial checks
    if len(l) != 3:
        raise ValueError("Provide a vector of three lengths")
    
    # Dependent modelling
    params = fk_dependent(l, a)

    # Independent modeling
    T = fk_independent(params)

    return T, params

##########################################
#  Inverse Kinematics
##########################################
def ik_dependent (xP):
    """
    Computes the dependent part of the inverse kinematic model of a three-wire PAUL using the PCC method.

    Parameters:
    xP (array): Position of the end (should be a vector of three positions).

    Returns:
    params (dict): Dictionary containing 'lr' (mean length), 'phi' (orientation), and 'kappa' (curvature).

    """

    # Initial checks
    if len(xP) < 3:
        raise ValueError("Provide a vector of, at least, three positions")
    
    # General case
    if np.sum(xP[:2] - np.array([0, 0])) != 0:
        phi = np.arctan2(xP[1], xP[0])
        kappa = 2 * np.linalg.norm(xP[:2]) / np.linalg.norm(xP)**2
        if xP[2] <= 0:
            theta = np.arccos(1 - kappa * np.linalg.norm(xP[:2]))
        else:
            theta = 2*np.pi - np.arccos(1 - kappa * np.linalg.norm(xP[:2]))
        theta2 = np.mod(theta + np.pi, 2*np.pi) - np.pi
        lr = abs(theta2 / kappa)

    # Singular configuration
    else:
        phi = 0  # Every value is possible
        kappa = 0
        lr = xP[2]

    params = {'lr': lr, 'phi': phi, 'kappa': kappa}

    return params

def ik_independent (params, phi0 = 0, a = 45):
    """
    Computes the independent part of the inverse kinematic model of a three-wire PAUL using the PCC method.

    Parameters:
    params (dict): Dictionary containing 'lr' (mean length), 'phi' (orientation), and 'kappa' (curvature).
    phi0 (float): Initial orientation angle. Optional.
    a (float): Diameter of the circumference formed by the cables. Optional.

    Returns:
    l (array): Lengths of the three wires.

    """

    # General case
    if params['phi'] and params['kappa']:
        phi_i = phi0 + np.array([np.pi, np.pi/3, -np.pi/3])
        l = params['lr'] * (1 + params['kappa'] * a * np.sin(params['phi'] + phi_i))

    # Singular configuration
    else:
        l = np.array(params['lr'], params['lr'], params['lr'])

    return l

def ik (xP, phi0 = 0, a = 45):
    """
    Computes the inverse kinematic model of a three-wire PAUL using the PCC method.

    Parameters:
    xP (array): Position of the end (should be a vector of three positions).
    phi0 (float): Initial orientation angle. Optional.
    a (float): Diameter of the circumference formed by the cables. Optional.

    Returns:
    l (array): Lengths of the three wires.
    params (dict): Dictionary containing 'lr' (mean length), 'phi' (orientation), and 'kappa' (curvature).

    """

    # Initial checks
    if len(xP) < 3:
        raise ValueError("Provide a vector of, at least, three positions")

    # Dependent modelling
    params = ik_dependent(xP)

    # Independent modelling
    l = ik_independent(params, phi0, a)

    return l, params
