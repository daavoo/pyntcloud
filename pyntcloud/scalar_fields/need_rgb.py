#  HAKUNA MATATA

"""
Scalar fields that require reed, green, blue
"""

import numpy as np

def rgb_intensity(rgb):
    rgb_i = rgb / np.sum(rgb, axis=1, keepdims=True) 
    return rgb_i[:,0], rgb_i[:,1], rgb_i[:,2]