#  HAKUNA MATATA

"""
VoxelGrid Class
"""

import numpy as np
import pandas as pd


class Octree(object):
    
    def __init__(self, points, max_level=2):
        self.points = points
        self.max_level= max_level
        self.structure =  pd.DataFrame(np.zeros((self.points.shape[0], self.max_level), dtype=np.uint8))
        xyzmin = points.min(0)
        xyzmax = points.max(0)
        #: adjust to obtain a  minimum bounding box with all sides of equal lenght 
        diff = max(xyzmax-xyzmin) - (xyzmax-xyzmin)
        xyzmin = xyzmin - diff / 2
        xyzmax = xyzmax + diff / 2
        self.xyzmin = xyzmin
        self.xyzmax = xyzmax
        self.id = "O({})".format(max_level)
        self.build()

    def build(self):
        self.sizes = np.zeros(self.max_level)
        level_ptp = max(self.xyzmax-self.xyzmin) / 2
        mid_points = np.zeros_like(self.points)
        mid_points[:] = (self.xyzmin + self.xyzmax) / 2

        for i in range(self.max_level):
            self.sizes[i] = level_ptp
            level_ptp /= 2
            bigger = self.points > mid_points

            if i != self.max_level - 1:
                mid_points = np.where(bigger, mid_points + level_ptp, mid_points - level_ptp)

            bigger = bigger.astype(np.uint8)
            self.structure.loc[:,i] = ((bigger[:,1] * 2) + bigger[:,0]) + (bigger[:,2] * (2 * 2))
    
    def get_centroids(self, level):
        st = self.structure.loc[:, range(level)]

        for n, i in enumerate(["x", "y", "z"]):
            st[i] = self.points[:, n]

        return st.groupby([x for x in range(level)], sort=False).mean().values
        
    def get_level_as_sf(self, level):
        sf = np.zeros((self.points.shape[0], level), dtype=str)
        
        for k, v in self.structure.groupby([x for x in range(level)]).indices.items():
            sf[v] = k

        return [int("".join(sf[i])) for i in range(len(sf))]

    def eigen_decomposition(self, level):
        st = self.structure.loc[:, range(level)]

        for n, i in enumerate(["x", "y", "z"]):
            st[i] = self.points[:, n]

        e_out = np.zeros((st.shape[0], 3))
        ev1_out = np.zeros((st.shape[0], 3))
        ev2_out = np.zeros((st.shape[0],3))
        ev3_out = np.zeros((st.shape[0],3))
        this_level = st.groupby([x for x in range(level)], sort=False)

        # to use when groups in current level have less than 3 points
        prev_level = st.groupby([x for x in range(level-1)], sort=False)
        min_level = prev_level
        min_i = 1
        # find the minimum level where there is no group with less than 3
        while min_level.size().min() < 3:
            min_i += 1
            min_level = st.groupby([x for x in range(level-min_i)])

        for n, g in this_level:

            if g.shape[0] < 3:
                g = prev_level.get_group(n[:-1])
                if g.shape[0] < 3:
                    g = min_level.get_group(n[:-min_i])

            eig_val, eig_vec = np.linalg.eig(np.cov(g.values[:,level:].T))
            idx = eig_val.argsort()[::-1] 
            eig_val = eig_val[idx]
            eig_vec = eig_vec[:,idx]
            e_out[g.index.values] = eig_val
            ev1_out[g.index.values] = eig_vec[:,0]
            ev2_out[g.index.values] = eig_vec[:,1]
            ev3_out[g.index.values] = eig_vec[:,2]

        return e_out[:,0], e_out[:,1], e_out[:,2], ev1_out, ev2_out, ev3_out




