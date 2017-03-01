
"""
HAKUNA MATATA
"""

from .scalar_fields import (
    is_plane,
    is_sphere,
    inclination_deg,
    inclination_rad,
    orientation_deg,
    orientation_rad,
    rgb_intensity,
    relative_luminance,
    hsv,
    octree_level,
    voxel_x,
    voxel_y,
    voxel_z,
    voxel_n,
    eigen_sum,
    omnivariance,
    eigenentropy,
    anisotropy,
    planarity,
    linearity,
    curvature,
    sphericity
)

SF_RANSAC = {
    'is_plane': (["is_plane"], is_plane),
    'is_sphere': (["is_sphere"], is_sphere)
}

SF_NORMALS = {
    'inclination_deg': (['inclination_deg'], inclination_deg),
    'inclination_rad': (['inclination_rad'], inclination_rad),
    'orientation_deg': (['orientation_deg'], orientation_deg),
    'orientation_rad': (['orientation_rad'],orientation_rad),
}

SF_RGB = {
    'rgb_intensity' : (['Ri', 'Gi', 'Bi'], rgb_intensity),
    'relative_luminance': (["relative_luminance"], relative_luminance),
    'hsv' : (['H', 'S', 'V'], hsv)
}

SF_OCTREE = {
    'octree_level': (['octree_level'], octree_level)
}

SF_VOXELGRID = {
    'voxel_x': (['voxel_x'], voxel_x),
    'voxel_y': (['voxel_y'], voxel_y),
    'voxel_z': (['voxel_z'], voxel_z),
    'voxel_n': (['voxel_n'], voxel_n)
}

SF_EIGENVALUES = {
    'eigen_sum': (['eigen_sum'], eigen_sum),
    'omnivariance': (['omnivariance'], omnivariance),
    'eigenentropy': (['eigenentropy'], eigenentropy),
    'anisotropy': (['anisotropy'], anisotropy),
    'planarity': (['planarity'] , planarity),
    'linearity': (['linearity'], linearity),
    'curvature': (['curvature'], curvature),
    'sphericity': (['sphericity'], sphericity)
}

ALL_SF = \
"""
ONLY POINTS
--------------
{}
{}

REQUIRE NORMALS 
---------------
{}
{}
{}
{}

REQUIRE RGB 
-----------
{}
{}
{}

REQUIRE OCTREE 
--------------
{}

REQUIRE VOXELGRID 
-----------------
{}
{}
{}
{}

REQUIRE EIGENVALUES
-------------------
{}
{}
{}
{}
{}
{}
{}
{}
""".format(
    *SF_RANSAC,
    *SF_NORMALS,
    *SF_RGB,
    *SF_OCTREE,
    *SF_VOXELGRID,
    *SF_EIGENVALUES
)



