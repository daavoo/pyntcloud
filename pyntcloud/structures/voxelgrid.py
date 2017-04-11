import numpy as np
from matplotlib import pyplot as plt
from scipy.spatial import cKDTree

from .base import Structure
from ..plot import plot_voxelgrid
from ..utils.array import cartesian
from ..utils.numba import groupby_max, groupby_count, groupby_sum


class VoxelGrid(Structure):
    
    def __init__(self, PyntCloud, x_y_z=[2, 2, 2], sizes=None, bb_cuboid=True):
        """
        Parameters
        ----------         
        points: (N,3) ndarray
            The point cloud from wich we want to construct the VoxelGrid.
            Where N is the number of points in the point cloud and the second
            dimension represents the x, y and z coordinates of each point.
        
        x_y_z :  list of int, optional
            Default: [2, 2, 2]
            The number of segments in wich each axis will be divided.
            x_y_z[0]: x axis 
            x_y_z[1]: y axis 
            x_y_z[2]: z axis
            If sizes is not None it will be ignored.
        
        sizes : list of float, optional
            Default: None
            The desired voxel size along each axis.
            sizes[0]: voxel size along x axis.
            sizes[1]: voxel size along y axis.
            sizes[2]: voxel size along z axis.

        bb_cuboid : bool, optional
            Default: True
            If True, the bounding box of the point cloud will be adjusted
            in order to have all the dimensions of equal lenght.                

        """
        super().__init__(PyntCloud)
        
        self.x_y_z = x_y_z
        self.sizes = sizes
        self.bb_cuboid = bb_cuboid
        
    def extract_info(self):
    
        points = self.points = self.PyntCloud.xyz
        
        xyzmin = points.min(0)
        xyzmax = points.max(0) 

        if self.bb_cuboid:
            #: adjust to obtain a  minimum bounding box with all sides of equal lenght 
            diff = max(xyzmax-xyzmin) - (xyzmax-xyzmin)
            xyzmin = xyzmin - diff / 2
            xyzmax = xyzmax + diff / 2 
        
        if self.sizes is not None:
            self.x_y_z = [1, 1, 1]
            for n, size in enumerate(self.sizes):
                if size is None:
                    continue
                margin = (((points.ptp(0)[n] // size) + 1) * size) - points.ptp(0)[n]
                xyzmin[n] -= margin / 2
                xyzmax[n] += margin / 2
                self.x_y_z[n] = ((xyzmax[n] - xyzmin[n]) / size).astype(int) 

        self.xyzmin = xyzmin
        self.xyzmax = xyzmax

        segments = []
        shape = []

        for i in range(3):
            # note the +1 in num 
            s, step = np.linspace(xyzmin[i], xyzmax[i], num=(self.x_y_z[i] + 1), retstep=True)
            segments.append(s)
            shape.append(step)
            
        self.segments = segments
        self.shape = shape
        
        self.n_voxels = self.x_y_z[0] * self.x_y_z[1] * self.x_y_z[2]
        
        self.n_x = self.x_y_z[0]
        self.n_y = self.x_y_z[1]
        self.n_z = self.x_y_z[2]
        
        self.id = "V({},{},{})".format(self.x_y_z, self.sizes, self.bb_cuboid)

    def compute(self):
        # find where each point lies in corresponding segmented axis
        # -1 so index are 0-based; clip for edge cases
        self.voxel_x = np.clip(np.searchsorted(self.segments[0], self.points[:,0]) - 1, 0, self.n_x)
        self.voxel_y = np.clip(np.searchsorted(self.segments[1], self.points[:,1]) - 1, 0, self.n_y)
        self.voxel_z = np.clip(np.searchsorted(self.segments[2], self.points[:,2]) - 1, 0, self.n_z) 
        self.voxel_n = np.ravel_multi_index([self.voxel_x, self.voxel_y, self.voxel_z], [self.n_x, self.n_y, self.n_z])

        # compute center of each voxel
        midsegments = [(self.segments[i][1:] + self.segments[i][:-1]) / 2 for i in range(3)]
        self.voxel_centers = cartesian(midsegments).astype(np.float32)
    
    def query(self, points):
        voxel_x = np.clip(np.searchsorted(self.segments[0], points[:,0]) - 1, 0, self.n_x)
        voxel_y = np.clip(np.searchsorted(self.segments[1], points[:,1]) - 1, 0, self.n_y)
        voxel_z = np.clip(np.searchsorted(self.segments[2], points[:,2]) - 1, 0, self.n_z) 
        voxel_n = np.ravel_multi_index([voxel_x, voxel_y, voxel_z], [self.n_x, self.n_y, self.n_z])
        
        return voxel_n
    
    def get_and_set(self):
        
        self.PyntCloud.voxelgrids[self.id] = self
        
        self.PyntCloud = None
        
        return self.id
    
    def get_feature_vector(self, mode="binary"):
        
        vector = np.zeros(self.n_voxels)
        
        if mode == "binary":
            vector[np.unique(self.voxel_n)] = 1
            return vector.reshape((self.n_x, self.ny, self.nz))

        elif mode == "density":
            count = np.bincount(self.voxel_n)
            vector[:len(count)] = count
            vector /= len(self.voxel_n)
            return vector.reshape((self.n_x, self.ny, self.nz))

        elif mode == "TDF":
            truncation = np.linalg.norm(self.shape)
            kdt = cKDTree(self.points)
            d, i =  kdt.query(self.voxel_centers, n_jobs=-1)
            return d.reshape((self.n_x, self.ny, self.nz))
        
        elif mode.endswith("_max"):
            N = {"x_max":0, "y_max":1, "z_max":2}
            return groupby_max(self.points, self.voxel_n, N[mode], vector)
        
        elif mode.endswith("_mean"):
            N = {"x_mean":0, "y_mean":1, "z_mean":2}
            s = np.zeros(self.n_voxels)
            c = np.zeros(self.n_voxels)
            return (np.nan_to_num(groupby_sum(self.points, self.voxel_n, N[mode], s) /
                    groupby_count(self.points, self.voxel_n, c)))
    

    def plot_feature_vector(self, mode="binary", d=2, cmap="Oranges"):
        feature_vector = self.get_feature_vector(mode)
        
        if d == 2:
            fig, axes= plt.subplots(int(np.ceil(self.n_z / 4)), 4, figsize=(8,8))
            plt.tight_layout()
            for i, ax in enumerate(axes.flat):
                if i >= len(feature_vector):
                    break
                im = ax.imshow(feature_vector[:, :, i], cmap=cmap, interpolation="none")
                ax.set_title("Level " + str(i))
            
        elif d == 3:
            return plot_voxelgrid(self, cmap=cmap)

