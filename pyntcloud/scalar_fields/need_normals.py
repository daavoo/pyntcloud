#  HAKUNA MATATA

"""
Scalar fields that require normals
"""

import numpy as np

def inclination_deg(normals):
    return np.rad2deg(np.arccos(normals[:,-1]))

def inclination_rad(normals):
    return np.arccos(normals[:,-1])

def orientation_deg(normals):
    angle = np.arctan2(normals[:,0], normals[:,1])
    #: convert (-180 , 180) to (0 , 360)
    angle = np.where(angle <0, angle + (2*np.pi), angle)
    return np.rad2deg(angle)

def orientation_rad(normals):
    angle = np.arctan2(normals[:,0], normals[:,1])
    #: convert (-PI , PI) to (0 , 2*PI)
    angle = np.where(angle <0, angle + (2*np.pi), angle)
    return angle



