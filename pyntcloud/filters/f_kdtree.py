
import numpy as np
from scipy.stats import zscore

def radious_outlier_removal(kdtree, points, k, r):
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

    distances = kdtree.query(points, k=k, n_jobs=-1)[0]
    ror_filter = np.all(distances < r, axis=1)

    return ror_filter

def statistical_outlier_removal(kdtree, points, k, z_max):
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

    distances, inidices = kdtree.query(points, k=k, n_jobs=-1)
    z_distances = zscore(np.mean(distances, axis=1), ddof=1)
    sor_filter = abs(z_distances) < z_max

    return sor_filter