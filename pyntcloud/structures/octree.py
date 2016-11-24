#  HAKUNA MATATA

"""
VoxelGrid Class
"""

import numpy as np
import pandas as pd

class Octree(object):
    
    def __init__(self, points, max_level=2, bb_cuboid=True, build=True):
        self.points = points
        self.max_level= max_level
        self.structure = pd.DataFrame(np.zeros((self.points.shape[0], self.max_level), dtype=np.uint8))
        xyzmin = points.min(0)
        xyzmax = points.max(0)

        if bb_cuboid:
            #: adjust to obtain a  minimum bounding box with all sides of equal lenght 
            diff = max(xyzmax-xyzmin) - (xyzmax-xyzmin)
            xyzmin = xyzmin - diff / 2
            xyzmax = xyzmax + diff / 2

        self.xyzmin = xyzmin
        self.xyzmax = xyzmax
        self.id = "O {}-{}".format(max_level, bb_cuboid)
        
        if build:
            self.build()

    def build(self, early_stop=True):
        level_ptp = np.ptp([self.xyzmin, self.xyzmax], axis=0) / 2
        mid_points = np.zeros_like(self.points)
        mid_points[:] = (self.xyzmin + self.xyzmax) / 2

        for i in range(self.max_level):
            level_ptp /= 2
            bigger = self.points > mid_points
            for j in range(3):                
                mid_points[:,j][bigger[:,j]] += level_ptp[j]
                mid_points[:,j][~bigger[:,j]] -= level_ptp[j]
            bigger = bigger.astype(np.uint8)
            self.structure.loc[:,i] = ((bigger[:,1] * 2) + bigger[:,0]) + (bigger[:,2] * (2 * 2))

            if early_stop and i > 1:
                columns = np.arange(i).tolist()
                less_than_2 = self.structure.ix[:, :i].groupby(columns).count().mean() < 2
                if less_than_2.any():
                    print("Stopping at level {}, less than 2 points in node".format(i))
                    self.structure = self.structure.ix[:,:i]
                    self.id = self.id.replace(str(self.max_level), str(i))
                    break
        return True
    
    def get_level_as_sf(self, level):
        sf = np.arange(len(self.points))
        i = 0

        for g in self.structure.groupby([x for x in range(level)]).apply(lambda x: x.index.values).values:
            sf[g] = i
            i+=1

        return sf

    def query(self, level):
        n_hood = [0] * len(self.points)

        for g in self.structure.groupby([x for x in range(level)]).apply(lambda x: x.index.values).values:
            for i in g:
                copy = g.tolist()
                copy.remove(i)
                n_hood[i] = copy

        return n_hood




