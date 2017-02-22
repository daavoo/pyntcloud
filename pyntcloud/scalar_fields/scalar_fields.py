#  HAKUNA MATATA


import numpy as np
from ..ransac import ransac
from ..geometry import Plane, Sphere

# RANSAC

def is_plane(points):
    return [ransac(points, Plane())]

def is_sphere(points):
    return [ransac(points, Sphere())]

# NEED NORMALS 

def inclination_deg(normals):
    return [np.rad2deg(np.arccos(normals[:,-1]))]

def inclination_rad(normals):
    return [np.arccos(normals[:,-1])]

def orientation_deg(normals):
    angle = np.arctan2(normals[:,0], normals[:,1])
    # convert (-180 , 180) to (0 , 360)
    angle = np.where(angle <0, angle + (2*np.pi), angle)
    return [np.rad2deg(angle)]

def orientation_rad(normals):
    angle = np.arctan2(normals[:,0], normals[:,1])
    # convert (-PI , PI) to (0 , 2*PI)
    angle = np.where(angle <0, angle + (2*np.pi), angle)
    return [angle]


# NEED RGB

def rgb_intensity(rgb):
    rgb_i = np.nan_to_num(rgb / np.sum(rgb, axis=1, keepdims=True)) 
    return rgb_i[:,0], rgb_i[:,1], rgb_i[:,2]

def relative_luminance(rgb):
    # relative luminance coeficients from Wikipedia
    return [np.einsum('ij, j', rgb, np.array([0.2125, 0.7154, 0.0721]))]

def hsv(rgb):
    MAX = np.max(rgb, -1)
    MIN = np.min(rgb, -1)
    MAX_MIN = np.ptp(rgb, -1)

    H = np.empty_like(MAX)
    
    idx = rgb[:,0] == MAX
    H[idx] = 60 * (rgb[idx, 1] - rgb[idx, 2]) / MAX_MIN[idx]
    H[np.logical_and(idx, rgb[:,1] < rgb[:,2])] += 360
    
    idx = rgb[:,1] == MAX
    H[idx] = (60 * (rgb[idx, 2] - rgb[idx, 0]) / MAX_MIN[idx]) + 120
    
    idx = rgb[:,2] == MAX
    H[idx] = (60 * (rgb[idx, 0] - rgb[idx, 1]) / MAX_MIN[idx]) + 240
    
    H = np.nan_to_num(H)
    S = np.nan_to_num(np.where(MAX == 0, 0, 1 - (MIN/MAX)))
    V = np.nan_to_num(MAX/255 * 100) 
    
    return H, S, V 


# NEED OCTREE

def octree_level(octree, level):
    if level > octree.max_level:
        raise ValueError(
            "The given level ({}) is higher than \
            octree.max_level ({})".format(level, octree.max_level))
    return [octree.get_level_as_sf(level)]

def eigen_octree(octree, level):
    return octree.eigen_decomposition(level)[:3]

def eigen_full_octree(octree, level):
    return octree.eigen_decomposition(level)


# NEED VOXELGRID

def voxel_x(voxelgrid):
    return [voxelgrid.structure[:,0]]

def voxel_y(voxelgrid):
    return [voxelgrid.structure[:,1]]

def voxel_z(voxelgrid):
    return [voxelgrid.structure[:,2]]

def voxel_n(voxelgrid):
    return [voxelgrid.structure[:,3]]

def eigen_voxelgrid(voxelgrid):
    return voxelgrid.eigen_decomposition()[:3]

def eigen_full_voxelgrid(voxelgrid):
    return voxelgrid.eigen_decomposition()  
    

# NEED KDTREE

def eigen_kdtree(kdtree, k):
    return kdtree.eigen_decomposition(k)[:3]

def eigen_full_kdtree(kdtree, k):
    e1, e2, e3, ev1, ev2, ev3 = kdtree.eigen_decomposition(k)
    ev1 = ev1.tolist()
    ev2 = ev2.tolist()
    ev3 = ev3.tolist()
    return e1, e2, e3, ev1, ev2, ev3

def normals_kdtree(kdtree, k):
    # kdtree.eigen_decomposition adapted to avoid unnecesary computations
    d, i = kdtree.query(kdtree.data, k=k, n_jobs=-1)
    neighbours = kdtree.data[i[:,1:]]
    diffs = neighbours - neighbours.mean(1,keepdims=True)
    cov_3D = np.einsum('ijk,ijl->ikl', diffs, diffs) / neighbours.shape[1]
    eigenvalues, eigenvectors = np.linalg.eig(cov_3D)
    sort = eigenvalues.argsort()
    # range from 0-shape[0] to allow indexing along axis 1 and 2
    idx_trick = range(eigenvalues.shape[0])
    unoriented_normals = eigenvectors[idx_trick, :, sort[:,0]] 

    # TODO orient normals

    return unoriented_normals
# NEED EIGENVALUES

def eigen_sum(ev):
    return [ev[:,0] + ev[:,1] + ev[:,2]]

def omnivariance(ev):
    return [(ev[:,0] * ev[:,1] * ev[:,2]) ** (1/3)]

def eigenentropy(ev):
    result = np.zeros(ev.shape[0])
    for i in range(3):
        result += ev[:,i] * np.log(ev[:,i])
    return [-result]

def anisotropy(ev):
    return [(ev[:,0] - ev[:,2]) / ev[:,0]]

def planarity(ev):
    return [(ev[:,1] - ev[:,2]) / ev[:,0]]

def linearity(ev):
    return [(ev[:,0] - ev[:,1]) / ev[:,0]]

def curvature(ev):
    return [ev[:,2] / (ev[:,0] + ev[:,1] + ev[:,2])]

def sphericity(ev):
    return [ev[:,2] / ev[:,0]]


# NEED EIGEN_VECTOR

def verticality(evec):
    return [1 - abs( evec[:,2].dot([0,0,1]))]




