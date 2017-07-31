import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from .base import Sampler


class Sampler_Voxelgrid(Sampler):
    """
    """

    def __init__(self, pyntcloud, voxelgrid):
        super().__init__(pyntcloud)
        self.voxelgrid = voxelgrid

    def extract_info(self):
        self.voxelgrid = self.pyntcloud.structures[self.voxelgrid]


class VoxelgridCenters(Sampler_Voxelgrid):
    """Returns the points that represent each occupied voxel's center."""
    def compute(self):
        return self.voxelgrid.voxel_centers[np.unique(self.voxelgrid.voxel_n)]


class VoxelgridCentroids(Sampler_Voxelgrid):
    """Returns the centroid of each group of points inside each occupied voxel."""
    def compute(self):
        df = pd.DataFrame(self.pyntcloud.xyz, columns=["x", "y", "z"])
        df["voxel_n"] = self.voxelgrid.voxel_n
        return df.groupby("voxel_n").mean().values


class VoxelgridNearest(Sampler_Voxelgrid):
    """Returns the point closest to each occupied voxel's center."""
    def compute(self):
        nonzero_centers = self.voxelgrid.voxel_centers[np.unique(
            self.voxelgrid.voxel_n)]
        kdt = cKDTree(self.pyntcloud.xyz)
        dist, nearest_indices = kdt.query(nonzero_centers, n_jobs=-1)
        return self.pyntcloud.points.ix[nearest_indices].reset_index(drop=True)
