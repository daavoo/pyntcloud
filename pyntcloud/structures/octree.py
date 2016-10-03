#  HAKUNA MATATA

"""
1 level Octree
"""
from .voxelgrid import VoxelGrid
import numpy as np


class Octree(VoxelGrid):
    
    def __init__(self, xyz, level, bb_cuboid=True):
        
        VoxelGrid.__init__(self, xyz, bb_cuboid)
        a = self.xyzmin
        b = self.xyzmax
        n = (2 ** level) + 1 
        #: get the segments divinding the 3 axis
        self.x, self.y, self.z = [np.linspace(a[i], b[i], n) for i in range(3)]
