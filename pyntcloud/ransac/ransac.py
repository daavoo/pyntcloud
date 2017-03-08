#  HAKUNA MATATA

"""
Ransac Implementation
"""

import numpy as np
import copy


def ransac( points, model, sampler, model_kwargs={}, sampler_kwargs={}, max_iterations=100, return_model=False):
    """ RANdom SAmple Consensus for fitting model to points.

    points : ndarray
        (N, M) ndarray where N is the number of points and M is the number
        scalar fields associated to each of those points. 
        M is usually 3 for representing the x, y, and z coordinates of each point.
    
    model : Ransac_Model
        Class (NOT INSTANCE!) representing the model that will be fitted to points. 
        Check ransac/models for reference.
    
    sampler : Ransac_Sampler
        Class (NOT INSTANCE!) used to sample points on each iteration. 
        Check ransac/samplers for reference.
    
    model_kwargs : dict, optional (default {})
        Arguments that will be used on model's instansiation.
        Variable according to passed model.
    
    sampler_kwargs : dict, optional (default {})
        Arguments that will be used on sampler's instansiation.
        Variable according to passed sampler.
    
    max_iterations : int, optional (default {})
        Maximum number of iterations.
    
    return_model : bool, optional (default False)
        Wheter the best fitted model will be returned or not.

    """

    model = model(**model_kwargs)
    sampler = sampler(points, model.k, **sampler_kwargs)

    n_best_inliers = 0        
    for i in range(max_iterations):

        k_points = sampler.get_sample()

        if not model.are_valid(k_points):
            continue

        model.fit(k_points)

        all_distances = model.get_distances(points)

        inliers = all_distances <= model.max_dist

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
 
