#  HAKUNA MATATA

import numpy as np


def random_sampling(points, n):

    return points[np.random.choice(points.shape[0], size=n)]

def mesh_sampling(mesh, n):
    pass