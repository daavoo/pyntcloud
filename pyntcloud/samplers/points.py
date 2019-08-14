from .base import Sampler
import random
import numpy as np
import pandas as pd


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


class FarthestPointsSampler(PointsSampler):
    """
    Parameters
    ----------
    n: int
        Number of unique points that will be chosen.
    """

    def __init__(self, *, pyntcloud, n, d_metric=np.diag([1., 1., 1.])):
        """d_metric -> Euclidean distance space by default, can be modified to other Mahalanobis distance as well"""
        super().__init__(pyntcloud=pyntcloud)
        self.n = n
        if not np.all(np.linalg.eigvals(d_metric) >= 0):
            raise ValueError("the Mahalanobis matrix must be positive semidefinite")
        self.d_metric = d_metric

    def cal_distance(self, point, solution_set):
        sum = 0
        for pt in solution_set:
            sum += np.dot(point[:3]-pt[:3], self.d_metric)
        return sum

    def compute(self):
        "incremental farthest search"
        if self.n > len(self.points):
            raise ValueError("n can't be higher than the number of points in the PyntCloud.")
        remaining_points = self.points.values
        solution_set = list()
        solution_set.append(remaining_points.pop(
            random.randint(0, len(remaining_points) - 1)))
        for _ in range(self.n - 1):
            distances = [self.cal_distance(p, solution_set[0]) for p in remaining_points]
            for i, p in enumerate(remaining_points):
                for j, s in enumerate(solution_set):
                    distances[i] = min(distances[i], self.cal_distance(p, s))
            solution_set.append(remaining_points.pop(distances.index(max(distances))))
        return pd.DataFrame(solution_set)
