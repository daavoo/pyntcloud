#  HAKUNA MATATA

"""
Ransac Implementation
"""

import numpy as np

def ransac(all_points, model, max_iterations=100, max_treshold=0):
    best_error = np.inf
    n_best_inliers = 0
        
    for i in range(max_iterations):
        k_points = all_points[np.random.randint(len(all_points), size=model.k)]
        model.fit(k_points)
        test_error = model.get_error(all_points)
        inliers = test_error <= max_treshold
        n_inliers = np.sum(inliers)

        if n_inliers > n_best_inliers:
            total_error = np.sum(test_error)

            if total_error < best_error:
                best_error = total_error
                best_inliers = inliers
         
    return best_inliers, model

 
