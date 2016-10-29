#  HAKUNA MATATA

import numpy as np
from scipy.stats import zscore


######################
# NEED NEIGHBOURHOOD #
######################
def radious_outlier_removal(n_hood, r):
    """ Compute a Radious Outlier Removal filter using the Neighbourhood.
    
    Parameters
    ----------                                    
    r: float
        The radius of the sphere with center on each point. The filter
        will look for the required number of neighboors inside that sphere.    
        
    Returns
    -------
    ror_filter : boolean array
        The boolean mask indicating wherever a point should be keeped or not.
        The size of the boolean mask will be the same as the number of points
        in the Neighbourhood.
        
    Notes
    -----          
    > The distances between each point and his 'k' nearest neighbors that 
        exceed the given 'r' are marked as False.
    
    > The points having any distance marked as False will be trimmed.
    
    The parameter r should be used in order to adjust the filter to
    the desired result.
            
    A LOWER 'r' value will result in a HIGHER number of points trimmed.
    """

    ror_filter = np.all(n_hood.distances > r, axis=1)

    return ror_filter, r

def statistical_outlier_removal(n_hood, z_max):
    """ Compute a Statistical Outlier Removal filter using the Neighbourhood.

    Parameters
    ----------  
    z_max: float
        The maximum Z score wich determines if the point is an outlier or 
        not.
        
    Returns
    -------
    sor_filter : boolean array
        The boolean mask indicating wherever a point should be keeped or not.
        The size of the boolean mask will be the same as the number of points
        in the Neighbourhood.
        
    Notes
    -----                
    > For each point, the mean of the distances between him and his 'k' nearest 
        neighbors is computed.
    
    > The Z score of those means is computed.
    
    >  Points where the Z score is less than or more than 'z_max' are marked
        as False, in order to be trimmed.    
    
    The optional parameter z_max should be used in order to adjust
    the filter to the desired result.
    
    A LOWER 'z_max' value will result in a HIGHER number of points trimmed.
    """

    z_distances = zscore(np.mean(n_hood.distances, axis=1), ddof=1)

    sor_filter = abs(z_distances) < z_max

    return sor_filter, z_max


############
# NEED XYZ #
############

def bounding_box(points, min_x=-np.inf, max_x=np.inf, min_y=-np.inf, max_y=np.inf, min_z=-np.inf, max_z=np.inf):
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
    
    parameters = ",".join([str(x) for x in [min_x, min_y, min_z, max_x, max_y, max_z]])
    return bb_filter, parameters

def random(points, size):

    filter = np.ones(points.shape[0], dtype=bool)

    filter[np.random.choice(points.shape[0], size=size)] = 0

    return filter, size


