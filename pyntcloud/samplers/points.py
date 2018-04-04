from .base import Sampler


class PointsSampler(Sampler):
    """
    """
    def extract_info(self):
        self.points = self.pyntcloud.points


class RandomPointsSampler(PointsSampler):
    """
    Parameters
    ----------
    n: int
        Number of unique points that will be chosen.
    """

    def __init__(self, *, pyntcloud, n):
        super().__init__(pyntcloud=pyntcloud)
        self.n = n

    def compute(self):
        if self.n > len(self.points):
            raise ValueError("n can't be higher than the number of points in the PyntCloud.")
        return self.points.sample(self.n).reset_index(drop=True)
