#  HAKUNA MATATA

"""
Other filters
""" 
import numpy as np

def pass_through(points, min_x=-np.inf, max_x=np.inf, min_y=-np.inf, max_y=np.inf,
              min_z=-np.inf, max_z=np.inf):
    """ Compute a Pass Through filter on the given points
    
    Parameters
    ----------                        
    points: (n,3) array
        The array containing all the points's coordinates. Expected format:
            array([
                [x1,y1,z1],
                ...,
                [xn,yn,zn]])
        
    min_i, max_i: float
        The bounding box limits for each coordinate. If some limits are missing,
        the default values are -infinite for the min_i and infinite for the max_i.
        
    Returns
    -------
    bb_filter : boolean array
        The boolean mask indicating wherever a point should be keeped or not.
        The size of the boolean mask will be the same as the number of given points.
        
    """

    bound_x = np.logical_and(points[:, 0] > min_x, points[:, 0] < max_x)
    bound_y = np.logical_and(points[:, 1] > min_y, points[:, 1] < max_y)
    bound_z = np.logical_and(points[:, 2] > min_z, points[:, 2] < max_z)
    
    bb_filter = np.logical_and(bound_x, bound_y, bound_z)
    
    return bb_filter

