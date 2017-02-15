
"""
HAKUNA MATATA
"""

from .scalar_fields import *

SF_RANSAC = {
    'is_plane': is_plane,
    'is_sphere': is_sphere
}

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
    'octree_level': octree_level,
    'eigen_octree': (['e1', 'e2', 'e3'], eigen_octree),
    'eigen_full_octree': (['e1', 'e2', 'e3', 'ev1', 'ev2', 'ev3'], eigen_full_octree)
}

SF_VOXELGRID = {
    'voxel_x': voxel_x,
    'voxel_y': voxel_y,
    'voxel_z': voxel_z,
    'voxel_n': voxel_n,
    'eigen_voxelgrid': (['e1', 'e2', 'e3'], eigen_voxelgrid),
    'eigen_full_voxelgrid': (['e1', 'e2', 'e3', 'ev1', 'ev2', 'ev3'], eigen_full_voxelgrid)
}

SF_KDTREE = {
    'eigen_kdtree': (['e1', 'e2', 'e3'], eigen_kdtree),
    'eigen_full_kdtree': (['e1', 'e2', 'e3', 'ev1', 'ev2', 'ev3'], eigen_full_kdtree)
}

SF_EIGENVALUES = {
    'eigen_sum': eigen_sum,
    'omnivariance': omnivariance,
    'eigenentropy': eigenentropy,
    'anisotropy': anisotropy,
    'planarity': planarity,
    'linearity': linearity,
    'curvature': curvature,
    'sphericity': sphericity
}

ALL_SF = "".join([" {}"] * 7).format(
    list(SF_RANSAC),
    list(SF_NORMALS),
    list(SF_RGB),
    list(SF_OCTREE),
    list(SF_VOXELGRID),
    list(SF_KDTREE),
    list(SF_EIGENVALUES)
)


