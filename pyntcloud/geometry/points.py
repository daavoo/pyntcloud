#  HAKUNA MATATA

"""
Points

"""
import numpy as np
import numba as nb
from math import atan2
from ..numba_functions.array import mean_axis0, array_minus_vector


def order_clockwise(points):
    
    angles = get_orientation(points)
    
    return points[np.argsort(angles)]


@nb.jit(nopython=True)   
def get_orientation(points):
    
    center = mean_axis0(points)
    
    to_center = array_minus_vector(points, center)
    
    angles = np.zeros(points.shape[0])
    
    for i in range(points.shape[0]):
        
        angle = atan2(to_center[i][0], to_center[i][1])
        
        if angle < 0:
            angle += 2 * np.pi
        
        angles[i] = angle 
        
    return angles