import numpy as np

def rgb_intensity(rgb):
    """ Red, green and blue intensity.
    
    Parameters
    ----------
    rgb: (N,3) ndarray
        Red, green and blue values.
    
    Returns
    -------
    r_i, g_i, b_i: (N,) ndarray
        Red, green and blue intensity as:
        r_i = (r / (r+g+b))
        g_i = (g / (r+g+b))
        b_i = (b / (r+g+b))
    """
    rgb_i = np.nan_to_num(rgb / np.sum(rgb, axis=1, keepdims=True)) 
    return rgb_i[:,0], rgb_i[:,1], rgb_i[:,2]

def relative_luminance(rgb):
    """ Similar to grayscale.
    
    Parameters
    ----------
    rgb: (N,3) ndarray
        Red, green and blue values.
    
    Returns
    -------
    relative_luminance: (N,) ndarray
        Computed following Wikipedia.
    """
    rgb /= 255.
    return [np.einsum('ij, j', rgb, np.array([0.2125, 0.7154, 0.0721]))]

def hsv(rgb):
    """ Hue, Saturation, Value colorspace.
    
    Parameters
    ----------
    rgb: (N,3) ndarray
        Red, green and blue values.
    
    Returns
    -------
    H, S, V: (N,) ndarray
        Computed following Wikipedia.
    """

    MAX = np.max(rgb, -1)
    MIN = np.min(rgb, -1)
    MAX_MIN = np.ptp(rgb, -1)

    H = np.empty_like(MAX)
    
    idx = rgb[:,0] == MAX
    H[idx] = 60 * (rgb[idx, 1] - rgb[idx, 2]) / MAX_MIN[idx]
    H[np.logical_and(idx, rgb[:,1] < rgb[:,2])] += 360
    
    idx = rgb[:,1] == MAX
    H[idx] = (60 * (rgb[idx, 2] - rgb[idx, 0]) / MAX_MIN[idx]) + 120
    
    idx = rgb[:,2] == MAX
    H[idx] = (60 * (rgb[idx, 0] - rgb[idx, 1]) / MAX_MIN[idx]) + 240
    
    H = np.nan_to_num(H)
    S = np.nan_to_num(np.where(MAX == 0, 0, 1 - (MIN/MAX)))
    V = np.nan_to_num(MAX/255 * 100) 
    
    return H, S, V 