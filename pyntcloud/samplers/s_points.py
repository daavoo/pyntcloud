from random import sample
from .base import Sampler


class Sampler_Points(Sampler):
    """
    """

    def __init__(self, pyntcloud):
        super().__init__(pyntcloud)

    def extract_info(self):
        self.points = self.pyntcloud.points


class RandomPoints(Sampler_Points):
    """ 'n' unique points randomly chosen

    Parameters
    ----------
    n: int
        Number of unique points that will be chosen.
    """

    def __init__(self, pyntcloud, n):
        super().__init__(pyntcloud)
        self.n = n

    def compute(self):

        indices = sample(range(0, self.points.shape[0]), self.n)
        return self.points.ix[indices].reset_index(drop=True)
