import numpy as np
import pandas as pd

from scipy.spatial import cKDTree

from .base import Sampler


class VoxelgridSampler(Sampler):
    def __init__(self, *, pyntcloud, voxelgrid_id):
        super().__init__(pyntcloud=pyntcloud)
        self.voxelgrid_id = voxelgrid_id

    def extract_info(self):
        self.voxelgrid = self.pyntcloud.structures[self.voxelgrid_id]


class VoxelgridCentersSampler(VoxelgridSampler):
    """Returns the points that represent each occupied voxel's center."""
    def compute(self):
        s = self.voxelgrid.voxel_centers[np.unique(self.voxelgrid.voxel_n)]
        return pd.DataFrame(s, columns=["x", "y", "z"])


class VoxelgridCentroidsSampler(VoxelgridSampler):
    """Returns the centroid of each group of points inside each occupied voxel."""
    def compute(self):
        df = pd.DataFrame(self.pyntcloud.xyz, columns=["x", "y", "z"])
        df["voxel_n"] = self.voxelgrid.voxel_n
        return df.groupby("voxel_n").mean()


class VoxelgridNearestSampler(VoxelgridSampler):
    """Returns the point closest to each occupied voxel's center."""
    def compute(self):
        nonzero_centers = self.voxelgrid.voxel_centers[np.unique(
            self.voxelgrid.voxel_n)]
        kdt = cKDTree(self.pyntcloud.xyz)
        distances, nearest_indices = kdt.query(nonzero_centers, n_jobs=-1)
        return self.pyntcloud.points.ix[nearest_indices].reset_index(drop=True)
