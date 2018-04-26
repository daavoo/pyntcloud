import numpy as np

from abc import ABC, abstractmethod
from ..structures import VoxelGrid


class RansacSampler(ABC):
    """ Base class for ransac samplers.

    Parameters
    ----------
    points : ndarray
        (N, M) ndarray where N is the number of points and M is the number
        scalar fields associated to each of those points.
        M is usually 3 for representing the x, y, and z coordinates of each point.

    k : int
        The number of points that will be sampled in each call of get_sample().
        This number depends on the model used. See ransac/models.py.
    """

    def __init__(self, points, k):
        self.points = points
        self.k = k

    @abstractmethod
    def get_sample(self):
        pass


class RandomSampler(RansacSampler):
    """ Sample random points.

    Inherits from RansacSampler.

    """

    def __init__(self, points, k):
        super().__init__(points, k)

    def get_sample(self):
        """ Get k unique random points.
        """
        sample = np.random.choice(len(self.points), self.k, replace=False)
        return self.points[sample]


class VoxelgridSampler(RansacSampler):
    """ Sample random points inside the same random voxel.

    Inherits from RansacSampler.

    Parameters
    ----------
    voxel_size : float, optional (default 0.1)

    """

    def __init__(self, points, k, voxel_size=0.1):
        super().__init__(points, k)
        sizes = [voxel_size] * 3
        self.voxelgrid = VoxelGrid(self.points, sizes=sizes, bb_cuboid=False)

    def get_sample(self):
        """ Get k unique random points from the same voxel of one randomly picked point.
        """
        # pick one point and get its voxel index
        idx = np.random.randint(0, len(self.points))
        voxel = self.voxelgrid.voxel_n[idx]

        # get index of points inside that voxel and convert to probabilities
        points_in_voxel = (self.voxelgrid.voxel_n == voxel).astype(int)
        points_in_voxel = points_in_voxel / points_in_voxel.sum()

        sample = np.random.choice(
            len(self.points), self.k, replace=False, p=points_in_voxel)

        return self.points[sample]
