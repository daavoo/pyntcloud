#  HAKUNA MATATA

import numpy as np


def random_sampling(points, n):

    return points[np.random.randint(0, points.shape[0], size=n)]


def mesh_sampling(triangles, n):
    
    areas = np.array([triangle_area(x) for x in triangles])
    # bigger triangles -> more probability to be selected
    probabilities = areas / np.sum(areas)
    random_idx = np.random.choice(np.arange(len(areas)), size=n, p=probabilities)
    new_points = np.zeros((n, triangles.shape[1]))

    for i in range(len(random_idx)):
        A, B, C = triangles[random_idx[i]]

        u, v = np.random.rand(2)
        if u + v > 1:
            u = 1 - u
            v = 1 - v

        new_points[i] = (A * u) + (B * v) + ((1 - (u+v)) * C)
    
    return new_points