#  HAKUNA MATATA

"""
Ransac Implementation
"""

import numpy as np
import copy

def ransac( points, model, filter=None, max_iterations=100,
            treshold=0.01, inliers_stop=np.inf, return_model=False):

    if filter is not None:
        points = points[filter]

    best_inliers = None
    n_best_inliers = 0        
    for i in range(max_iterations):

        k_points = points[ np.random.randint(len(points), size=model.k) ]
        if not model.are_valid(k_points):
            continue

        model.fit(k_points)
        all_error = model.get_error(points)
        inliers = all_error <= treshold
        n_inliers = np.sum(inliers)
        
        if n_inliers > n_best_inliers:
            n_best_inliers = n_inliers
            best_inliers = inliers
            if return_model:
                best_model = copy.deepcopy(model)

    if return_model:
        return best_inliers, best_model
    else:
        return best_inliers
 
