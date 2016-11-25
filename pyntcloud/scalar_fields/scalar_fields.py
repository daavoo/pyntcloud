#  HAKUNA MATATA


import numpy as np


# NEED NORMALS 

def inclination_deg(normals):
    return np.rad2deg(np.arccos(normals[:,-1]))

def inclination_rad(normals):
    return np.arccos(normals[:,-1])

def orientation_deg(normals):
    angle = np.arctan2(normals[:,0], normals[:,1])
    # convert (-180 , 180) to (0 , 360)
    angle = np.where(angle <0, angle + (2*np.pi), angle)
    return np.rad2deg(angle)

def orientation_rad(normals):
    angle = np.arctan2(normals[:,0], normals[:,1])
    # convert (-PI , PI) to (0 , 2*PI)
    angle = np.where(angle <0, angle + (2*np.pi), angle)
    return angle


# NEED RGB

def rgb_intensity(rgb):
    rgb_i = rgb / np.sum(rgb, axis=1, keepdims=True) 
    return rgb_i[:,0], rgb_i[:,1], rgb_i[:,2]

def relative_luminance(rgb):
    # relative luminance coeficients from Wikipedia
    return np.einsum('ij, j', rgb, np.array([0.2125, 0.7154, 0.0721]))

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
    
    S = np.where(MAX == 0, 0, 1 - (MIN/MAX))
    V = MAX/255 * 100 
    
    return H, S, V 


# NEED EIGENVALUES

def eigen_sum(structure):
    ev1, ev2, ev3 = structure.eig_val1, structure.eig_val2, structure.eig_val3
    return ev1 + ev2 + ev3

def omnivariance(structure):
    ev1, ev2, ev3 = structure.eig_val1, structure.eig_val2, structure.eig_val3
    return (ev1 * ev2 * ev3) ** (1/3)

def eigenentropy(structure):
    ev = structure.eig_val1, structure.eig_val2, structure.eig_val3
    result = np.zeros_like(eig_val1)
    for i in range(3):
        result += ev[i] * np.log(ev[i])
    return - result

def anisotropy(structure):
    ev1, ev3 = structure.eig_val1, structure.eig_val3
    return (ev1 - ev3) / ev1

def planarity(structure):
    ev1, ev2, ev3 = structure.eig_val1, structure.eig_val2, structure.eig_val3
    return (ev2 - ev3) / ev1

def linearity(structure):
    ev1, ev2, ev3 = structure.eig_val1, structure.eig_val2, structure.eig_val3
    return (ev1 - ev2) / ev1

def curvature(structure):
    ev1, ev2, ev3 = structure.eig_val1, structure.eig_val2, structure.eig_val3
    return ev3 / (ev1 + ev2 + ev3)

def sphericity(structure):
    ev1, ev3 = structure.eig_val1, structure.eig_val3
    return ev3 / ev1

def verticality(structure):
    evc3 = structure.eig_vec3
    return 1 - abs( evc3.dot([0,0,1]) )


# NEED OCTREE

def octree_level(octree, level):
    if level > octree.max_level:
        raise ValueError("The given level ({}) is higher than octree.max_level ({})".format(level, octree.max_level))
    return octree.get_level_as_sf(level)


# NEED VOXELGRID

def voxel_x(voxelgrid):
    return voxelgrid.structure.voxel_x

def voxel_y(voxelgrid):
    return voxelgrid.structure.voxel_y

def voxel_z(voxelgrid):
    return voxelgrid.structure.voxel_z

def voxel_n(voxelgrid):
    return voxelgrid.structure.voxel_n

