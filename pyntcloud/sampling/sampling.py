#  HAKUNA MATATA

import numpy as np


def random_sampling(points, size):

    sampled = np.ones(points.shape[0], dtype=bool)

    sampled[np.random.choice(points.shape[0], size=size)] = 0

    return sampled