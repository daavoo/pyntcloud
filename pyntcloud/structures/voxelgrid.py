#  HAKUNA MATATA

"""
VoxelGrid Main Class
"""

import numpy as np
import pandas as pd
from numba import jit


class VoxelGrid(object):
    
    def __init__(self, xyz, bb_cuboid=True):
        """
        Parameters
        ----------         
        xyz: (N,3) ndarray
            The point cloud from wich we want to construct the octree.
            Where N is the number of points in the point cloud and the second
            dimension represents the x, y and z coordinates of each point.
        
        bb_cuboid(Optional): bool
            If True(Default): The bounding box of the point cloud will be adjusted
                in order to have all the dimensions of equal lenght.
                
            If False: The bounding box is allowed to have dimensions of different
                sizes.
        """
        self.xyz = xyz
        xyzmin = np.min(xyz,axis=0) 
        xyzmax = np.max(xyz,axis=0) 
        
        if bb_cuboid:
            diff = max(xyzmax-xyzmin) - (xyzmax-xyzmin)
            #: adjust to obtain a  minimum bounding box with all sides of equal lenght 
            xyzmin = xyzmin - diff / 2
            xyzmax = xyzmax + diff / 2
            
        self.xyzmin = xyzmin
        self.xyzmax = xyzmax
    
    def build(self):
        x = self.x
        y = self.y
        z = self.z
        x_centroids = get_centroids(x)
        y_centroids = get_centroids(y)
        z_centroids = get_centroids(z)
        self.structure = self.get_structure(x, y, z, x_centroids, y_centroids, z_centroids)           
            
    def get_structure(self, x, y, z, xc, yc, zc):
        xyz = self.xyz
        #: a multiple index array (N,3) wich will store values for each corresponding
        # segment for each corresponding axis where a point lies.
        mul_idx = np.zeros_like(xyz, dtype=int)
        
        #: an unique index array (N) wich will store values for each corresponding
        # voxel where a point lies.
        uni_idx = np.zeros(xyz.shape[0], dtype=int)
        
        #: an (N,3) array wich will store the x, y, z values of the centroid of
        # each corresponding voxel where a point lies.
        centroids = np.zeros_like(xyz)
        
        fill_idx_centroids(xyz, x, y, z, mul_idx, uni_idx, xc, yc, zc, centroids)
        
        #: convert the arrays into pandas Dataframe
        mul_idx = pd.DataFrame(mul_idx, columns=['voxel_x','voxel_y','voxel_z'], dtype=float)
        uni_idx = pd.DataFrame(uni_idx, columns=['voxel_n'], dtype=float)
        centroids = pd.DataFrame(centroids, columns=['centroid_x','centroid_y','centroid_z'], dtype=float)
        structure = pd.concat([mul_idx, centroids, uni_idx], axis=1)     
        return structure   
        
    def get_percentages(self):
        #: array full of zeros with size equal to the total number of voxels
        zero_percent = pd.Series(np.zeros((2 ** self.n) ** 3))
        #: corresponding percentages of points for each voxel
        percent = self.structure['voxel_n'].value_counts(sort=False) / len(self.xyz)
        #: just fill the array of zeros in the places where correspond.
        percent = zero_percent.add(percent, fill_value=0)     
        return percent     
        
      
@jit(nopython=True)
def fill_idx_centroids(xyz, x, y, z, mul_idx, uni_idx, cx, cy, cz, centroids):
    """ Fill the empty arrays of indexes with the corresponding indexes for each point.
    
    Parameters
    ----------         
    xyz: (N,3) ndarray
        The point cloud from wich we want to compute the indexes.
        Where N is the number of points in the point cloud and the second
        dimension represents the x, y and z coordinates of each point.
    
    x, y, z:  ndarray
        The segments along the 'x', 'y' and 'z' axis. The number of segments 'M'
        is derived from the level of subdivision 'n'.
    
    mul_idx: (N,3) ndarray
        An empty array that will be filled with the number of each corresponding
        segment for each corresponding axis for all the points in xyz.  

    uni_idx: (N,) ndarray
        An empty array that will be filled with the number of the corresponding
        voxel.   
    
    cx, cy, cz:  ndarray
        The centroids of the segments.
        
    centroids: (N,3)
        An empty array that will store the x, y, z values of the centroid of
        each corresponding voxel where a point lies.
    """
    
    #: use -1 because linspace takes as an argument the number of segments + 1
    nx = len(x) - 1
    ny = len(y) - 1
    for i in range(len(xyz)):
        for j in range(len(x)):  
            
            if xyz[i,0] >= x[j] and xyz[i,0] <= x[j+1]:                
                for k in range(len(y)):  
                    
                    if xyz[i,1] >= y[k] and xyz[i,1] <= y[k+1]:                        
                        for l in range(len(z)):  
                            
                            if xyz[i,2] >= z[l] and xyz[i,2] <= z[l+1]:                                
                                #: use +1 because I want an "1 based index"
                                mul_idx[i,0] = j+1
                                mul_idx[i,1] = k+1
                                mul_idx[i,2] = l+1   
                                
                                centroids[i,0] = cx[j]
                                centroids[i,1] = cx[k]
                                centroids[i,2] = cx[l]
                                
                                #: I'llprobably need to explain this conversion
                                # graphically in the online documentation.
                                uni_idx[i] = (nx * j) + k + (nx * ny * l)                                
                                break
                        break
                break
            

@jit(nopython=True)
def get_centroids(segments):
    
    centroids = np.zeros(len(segments) -1)
    for i in range(1, len(segments)):
        centroids[i -1] = (segments[i-1] + segments[i]) / 2
    
    return centroids
    
