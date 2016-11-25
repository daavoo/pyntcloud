
"""
HAKUNA MATATA
"""

from .scalar_fields import *

SF_NORMALS = {
'inclination_deg': inclination_deg,
'inclination_rad': inclination_rad,
'orientation_deg': orientation_deg,
'orientation_rad': orientation_rad,
}

SF_RGB = {
'rgb_intensity' : (['Ri', 'Gi', 'Bi'], rgb_intensity),
'relative_luminance': relative_luminance,
'hsv' : (['H', 'S', 'V'], hsv)
}

SF_OCTREE = {
'octree_level': octree_level
}

SF_VOXELGRID = {
'voxel_x': voxel_x,
'voxel_y': voxel_y,
'voxel_z': voxel_z,
'voxel_n': voxel_n
}

SF_KDTREE = {
'eigen_kdtree': ['e1', 'e2', 'e3'],
'eigen_full_kdtree': ['e1', 'e2', 'e3', 'ev1', 'ev2', 'ev3']
}

SF_OCTREE_LEVEL = {
'eigen_octree_level': ['e1', 'e2', 'e3'],
'eigen_full_octree_level': ['e1', 'e2', 'e3', 'ev1', 'ev2', 'ev3']
}

SF_VOXEL_N = {
'eigen_voxel_n': ['e1', 'e2', 'e3'],
'eigen_full_voxel_n': ['e1', 'e2', 'e3', 'ev1', 'ev2', 'ev3']
}

SF_EIGENVALUES = {
'eigen_sum': eigen_sum,
'omnivariance': omnivariance,
'eigenentropy': eigenentropy,
'anisotropy': anisotropy,
'planarity': planarity,
'linearity': linearity,
'curvature': curvature,
'sphericity': sphericity,
'verticality':verticality
}

ALL_SF = "{}  {}  {}  {}  {}  {}  {}".format(
    SF_NORMALS.keys(),
    SF_RGB.keys(),
    SF_OCTREE.keys(),
    SF_VOXELGRID.keys(),
    SF_KDTREE.keys(),
    SF_OCTREE_LEVEL.keys(),
    SF_VOXEL_N.keys(),
    SF_EIGENVALUES.keys()
)


