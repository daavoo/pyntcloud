
"""
HAKUNA MATATA
"""

from .sf_eigenvalues import (
    anisotropy,
    curvature,
    eigenentropy,
    eigen_sum,
    linearity,
    omnivariance,
    planarity,    
    sphericity
)
from .sf_normals import (
    inclination_deg,
    inclination_rad,
    orientation_deg,
    orientation_rad
)
from .sf_rgb import (
    hsv,
    relative_luminance,
    rgb_intensity
)
from .sf_voxelgrid import (
    voxel_n,
    voxel_x,
    voxel_y,
    voxel_z
)
from .sf_xyz import (
    is_plane,
    is_sphere
)

SF_EIGENVALUES = {
    'anisotropy': (['anisotropy'], anisotropy),
    'curvature': (['curvature'], curvature),
    'eigenentropy': (['eigenentropy'], eigenentropy),
    'eigen_sum': (['eigen_sum'], eigen_sum),
    'linearity': (['linearity'], linearity),
    'omnivariance': (['omnivariance'], omnivariance),    
    'planarity': (['planarity'] , planarity),  
    'sphericity': (['sphericity'], sphericity)
}

SF_NORMALS = {
    'inclination_deg': (['inclination_deg'], inclination_deg),
    'inclination_rad': (['inclination_rad'], inclination_rad),
    'orientation_deg': (['orientation_deg'], orientation_deg),
    'orientation_rad': (['orientation_rad'],orientation_rad),
}

SF_RGB = {
    'hsv' : (['H', 'S', 'V'], hsv),
    'relative_luminance': (["relative_luminance"], relative_luminance),
    'rgb_intensity' : (['Ri', 'Gi', 'Bi'], rgb_intensity)    
}

SF_VOXELGRID = {
    'voxel_n': (['voxel_n'], voxel_n),
    'voxel_x': (['voxel_x'], voxel_x),
    'voxel_y': (['voxel_y'], voxel_y),
    'voxel_z': (['voxel_z'], voxel_z)
}

SF_XYZ = {
    'is_plane': (["is_plane"], is_plane),
    'is_sphere': (["is_sphere"], is_sphere)
}

ALL_SF = \
"""
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

REQUIRE VOXELGRID 
-----------------
{}
{}
{}
{}

REQUIRE XYZ
--------------
{}
{}

""".format(
    *SF_EIGENVALUES,
    *SF_NORMALS,
    *SF_RGB,
    *SF_VOXELGRID,
    *SF_XYZ    
)



