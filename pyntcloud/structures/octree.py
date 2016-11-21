#  HAKUNA MATATA

"""
VoxelGrid Class
"""

import numpy as np


class OcTree(object):
    
    def __init__(self, points, max_level=2, build=True):
        """
        Parameters
        ----------         
        points: (N,3) ndarray
                The point cloud from wich we want to construct the VoxelGrid.
                Where N is the number of points in the point cloud and the second
                dimension represents the x, y and z coordinates of each point.
                
        """
        self.points = points
        self.max_level= max_level
        self.structure = np.zeros((self.points.shape[0], self.max_level))
        
        if build:
            self.build()

    def build(self):

        level_ptp = self.points.ptp(0) / 4

        mid_points = np.zeros_like(self.points)
        mid_points[:] = (self.points.min(0) + self.points.max(0)) / 2

        for i in range(self.max_level):

            bigger = self.points > mid_points

            for j in range(3):
                mid_points[:,j][bigger[:,j]] += level_ptp[j]
                mid_points[:,j][~bigger[:,j]] -= level_ptp[j]

            bigger = bigger.astype(np.uint8)

            # i = ((y * n_x) + x) + (z * (n_x * n_y))
            self.structure[:,i] = ((bigger[:,1] * 2) + bigger[:,0]) + (bigger[:,2] * (2 * 2))

            level_ptp /= 2




