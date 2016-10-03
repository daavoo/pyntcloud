#  HAKUNA MATATA

"""
VoxelGrid of fixed voxel size
"""
from .voxelgrid import VoxelGrid
import numpy as np


class FixedSizeVoxelGrid(VoxelGrid):
    
    def __init__(self, xyz, size, bb_cuboid=True):
        
        VoxelGrid.__init__(self, xyz, bb_cuboid)
        a = self.xyzmin
        b = self.xyzmax
        #: get the segments divinding the 3 axis
        self.x, self.y, self.z = [np.linspace(a[i], b[i], (b[i]- a[i]) / size) for i in range(3)]
