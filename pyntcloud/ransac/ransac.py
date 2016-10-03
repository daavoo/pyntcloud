#  HAKUNA MATATA

"""
Ransac Implementation
"""

import numpy as np
from numba import jit

@jit(nopython=True)
def ransac(all_points, model, max_iterations=100, max_treshold=0):
    
    #: Initialize with a inf. error and 0 inliers to ensure that the first iteration will
    # be an improvement.
    best_error = np.inf
    n_best_inliers = 0
        
    for i in range(max_iterations):
        
        #: see random_subset()
        k_points = random_subset(model.k, all_points)
        
        #: there is no asignation because the attributes of the ransac-model object
        # will be updated with the fit function.
        model.fit(k_points)
        
        #: error for all the set
        test_error = model.get_error(all_points)
        
        inliers = test_error <= max_treshold
        
        n_inliers = np.sum(inliers)
        
        #: if this random sample has less inliers than the best one -> discard sample
        if n_inliers > n_best_inliers:
                        
            #: get the distances with all the points
            total_error = np.sum(test_error)
            
            #: if this random sample has more error than the best one -> discard sample
            if total_error < best_error:
                
                best_error = total_error
                best_inliers = inliers
         
    return best_inliers, model
                
                
@jit(nopython=True)             
def random_subset(n, X):
    """ Get a subset of size n from the data
    """
    idx = np.random.choice(len(X), n)

    return X[idx]  
 
