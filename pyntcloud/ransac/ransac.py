#  HAKUNA MATATA

"""
Ransac Implementation
"""

import numpy as np

def ransac( points, model, filter=None, max_iterations=100,
            treshold=0.01, inliers_stop=np.inf, error_stop=0,
            return_model=False):

    if filter is not None:
        points = points[filter]

    best_error = np.inf
    n_best_inliers = 0        
    for i in range(max_iterations):
        k_points = points[np.random.randint(len(points), size=model.k)]
        if model.are_invalid(k_points):
            continue
        model.fit(k_points)
        individual_error = model.get_error(points)
        inliers = individual_error <= treshold
        n_inliers = np.sum(inliers)

        if n_inliers > n_best_inliers:
            n_best_inliers = n_inliers
            total_error = np.sum(individual_error)
            
            if total_error < best_error:
                best_error = total_error
                best_inliers = inliers
    
    if return_model:
        return best_inliers, model
    
    return best_inliers
 
