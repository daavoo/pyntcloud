#  HAKUNA MATATA

"""
Ransac Implementation
"""

import numpy as np

def ransac(points, model, filter=None, max_iterations=100, max_treshold=0):
    if filter is not None:
        points = points[filter]
    best_error = np.inf
    n_best_inliers = 0
        
    for i in range(max_iterations):
        k_points = points[np.random.randint(len(points), size=model.k)]
        model.fit(k_points)
        test_error = model.get_error(points)
        inliers = test_error <= max_treshold
        n_inliers = np.sum(inliers)

        if n_inliers > n_best_inliers:
            total_error = np.sum(test_error)

            if total_error < best_error:
                best_error = total_error
                best_inliers = inliers
         
    return best_inliers, model

 
