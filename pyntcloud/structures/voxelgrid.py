#  HAKUNA MATATA

"""
VoxelGrid Main Class
"""

import numpy as np
from matplotlib import pyplot as plt


class VoxelGrid(object):
    
    def __init__(self, points, x_y_z=[1, 1, 1], bb_cuboid=True, build=True):
        """
        Parameters
        ----------         
        points: (N,3) ndarray
                The point cloud from wich we want to construct the VoxelGrid.
                Where N is the number of points in the point cloud and the second
                dimension represents the x, y and z coordinates of each point.
        
        x_y_z:  list
                The segments in wich each axis will be divided.
                x_y_z[0]: x axis 
                x_y_z[1]: y axis 
                x_y_z[2]: z axis

                if x_y_z[i] is an int then -> np.linspace(xyzmin[i], xyzmax[i],
                                                             num=(x_y_z[i] + 1))

                if x_y_z[i] is an array then the values will be used as segments.

        bb_cuboid(Optional): bool
                If True(Default):   
                    The bounding box of the point cloud will be adjusted
                    in order to have all the dimensions of equal lenght.                
                If False:
                    The bounding box is allowed to have dimensions of different sizes.
        """
        self.points = points

        xyzmin = np.min(points, axis=0) 
        xyzmax = np.max(points, axis=0)

        if bb_cuboid:
            #: adjust to obtain a  minimum bounding box with all sides of equal lenght 
            diff = max(xyzmax-xyzmin) - (xyzmax-xyzmin)
            xyzmin = xyzmin - diff / 2
            xyzmax = xyzmax + diff / 2
        
        self.xyzmin = xyzmin
        self.xyzmax = xyzmax

        segments = []

        for i in range(3):
            if type(x_y_z[i]) is int:
                # note the +1 in num 
                segments.append(np.linspace(xyzmin[i], xyzmax[i], num=(x_y_z[i] + 1)))
            else:
                # clip in case the given segments exceed the bounding box
                segments.append(np.clip(x_y_z[i], xyzmin[i], xyzmax[i])) 
        
        self.segments = segments
        
        self.n_voxels = (len(segments[0]) -1) * (len(segments[1]) -1) * (len(segments[2]) -1)
        if build:
            self.build()

    def build(self):

        structure = np.zeros((len(self.points), 4), dtype=int)

        structure[:,0] = np.argmin(self.points[:,0,np.newaxis] > self.segments[0], axis=1) 
        structure[:,0] = np.where(structure[:,0] !=0, structure[:,0] -1, 0 )

        structure[:,1] = np.argmin(self.points[:,1,np.newaxis] > self.segments[1], axis=1) 
        structure[:,1] = np.where(structure[:,1] !=0, structure[:,1] -1, 0 )

        structure[:,2] = np.argmin(self.points[:,2,np.newaxis] > self.segments[2], axis=1)
        structure[:,2] = np.where(structure[:,2] !=0, structure[:,2] -1, 0 )

        # convert voxel_x , voxel_y, voxel_z into a single voxel_n
        n_x = len(self.segments[0]) - 1
        n_y = len(self.segments[1]) - 1
        structure[:,3] = (structure[:,0] * n_x) + structure[:,1] + (n_x * n_y * structure[:,2])
        
        self.structure = structure

        self.vector = np.bincount(np.concatenate((self.structure[:,3], np.arange(self.n_voxels)))) -1
 
    def plot(self):
        n_x = int(len(self.segments[0]) - 1)
        n_y = int(len(self.segments[1]) - 1)
        n_z = int(len(self.segments[2]) - 1)

        fig, axes= plt.subplots(int(np.ceil(n_z / 4)), 4, figsize=(8,8))

        plt.tight_layout()

        imgs = self.vector.reshape([n_x, n_y, n_z])

        for i,ax in enumerate(axes.flat):
            if i >= len(imgs):
                break
            im = ax.imshow(imgs[i], cmap="YlOrRd", interpolation="none")
            ax.set_title("Level " + str(i))

        fig.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
        cbar = fig.colorbar(im, cax=cbar_ax)
        cbar.set_label('NUMBER OF POINTS IN VOXEL')
