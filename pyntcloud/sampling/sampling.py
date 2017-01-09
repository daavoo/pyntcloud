#  HAKUNA MATATA

import numpy as np


def random_sampling(points, size):

    return points[np.random.choice(points.shape[0], size=size)]
    