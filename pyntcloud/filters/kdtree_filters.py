#  HAKUNA MATATA

"""
KDTree filters
"""

import numpy as np
from scipy import stats


def statistical_outilier_removal(kdtree, k=8, z_max=2 ):
    """ Compute a Statistical Outlier Removal filter on the given KDTree.
    
    Parameters
    ----------                        
    kdtree: scipy's KDTree instance
        The KDTree's structure which will be used to
        compute the filter.
        
    k(Optional): int
        The number of nearest neighbors wich will be used to estimate the 
        mean distance from each point to his nearest neighbors.
        Default : 8
        
    z_max(Optional): int
        The maximum Z score wich determines if the point is an outlier or 
        not.
        
    Returns
    -------
    sor_filter : boolean array
        The boolean mask indicating wherever a point should be keeped or not.
        The size of the boolean mask will be the same as the number of points
        in the KDTree.
        
    Notes
    -----
    > The filter computes the distances between each point and his 'k' nearest 
        neighbors.
        
    > The mean of those distances is computed for each point.
    
    > The Z score of those means is computed.
    
    > The points where the Z score is less than or more than 'z_max' are marked
        as False, in order to be trimmed.    
    
    The 2 optional parameters (k and z_max) should be used in order to adjust
    the filter to the desired result.
    
    A HIGHER 'k' value will result(normally) in a HIGHER number of points trimmed.
    
    A LOWER 'z_max' value will result(normally) in a HIGHER number of points trimmed.
    
    """
    
    distances, i = kdtree.query(kdtree.data, k=k, n_jobs=-1) 
    
    z_distances = stats.zscore(np.mean(distances, axis=1))
    
    sor_filter = abs(z_distances) < z_max
    
    return sor_filter
    
def radious_outlier_removal(kdtree, k, r):
    """ Compute a Radious Outlier Removal filter on the given KDTree
    
    Parameters
    ----------                        
    kdtree: scipy's KDTree instance
        The KDTree's structure which will be used to
        compute the filter.
        
    k: int
        The number of nearest neighbors wich will be used to estimate the 
        mean distance from each point to his nearest neighbors.
        
    r: float
        The radius of the sphere with center on each point and where the filter
        will look for the required number of k neighboors.    
        
    Returns
    -------
    ror_filter : boolean array
        The boolean mask indicating wherever a point should be keeped or not.
        The size of the boolean mask will be the same as the number of points
        in the KDTree.
        
    Notes
    -----
    > The filter computes the distances between each point and his 'k' nearest 
        neighbors.
        
    > The distances exceeding the given 'r' are marked as inf.
    
    > The points having any inf distance are marked as False, in order to be
        trimmed.
    
    The 2 parameters (k and r) should be used in order to adjust the filter to
    the desired result.
    
    A HIGHER 'k' value will result(normally) in a HIGHER number of points trimmed.
    
    A LOWER 'r' value will result(normally) in a HIGHER number of points trimmed.
    
    """
    
    distances, i = kdtree.query(kdtree.data, k=k, distance_upper_bound=r, n_jobs=-1) 
    
    ror_filter = np.any(np.isinf(distances), axis=1)
    
    return ror_filter