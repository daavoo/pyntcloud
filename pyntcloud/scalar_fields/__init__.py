from .sf_eigenvalues import (
    Anisotropy,
    Curvature,
    Eigenentropy,
    EigenSum,
    Linearity,
    Omnivariance,
    Planarity,    
    Sphericity
)
from .sf_kneighbors import (
    EigenDecomposition,
    EigenValues
)
from .sf_normals import (
    InclinationDegrees,
    InclinationRadians,
    OrientationDegrees,
    OrientationRadians
)
from .sf_rgb import (
    HSV,
    RelativeLuminance,
    RGBIntensity
)
from .sf_voxelgrid import (
    VoxelN,
    VoxelX,
    VoxelY,
    VoxelZ,
    EuclideanClusters
)
from .sf_xyz import (
    PlaneFit,
    SphereFit,
    CustomFit
)
ALL_SF = {
    # Eigenvalues
    'anisotropy': Anisotropy,
    'curvature': Curvature,
    'eigenentropy': Eigenentropy,
    'eigen_sum': EigenSum,
    'linearity': Linearity,
    'omnivariance': Omnivariance,    
    'planarity': Planarity, 
    'sphericity': Sphericity,
    # Kneighbors
    'eigen_decomposition': EigenDecomposition,
    'eigen_values': EigenValues, 
    # Normals
    'inclination_deg': InclinationDegrees,
    'inclination_rad': InclinationRadians,
    'orientation_deg': OrientationDegrees,
    'orientation_rad': OrientationRadians,
    # RGB
    'hsv': HSV,
    'relative_luminance': RelativeLuminance,
    'rgb_intensity': RGBIntensity,
    # Voxelgrid
    'voxel_n': VoxelN,
    'voxel_x': VoxelX,
    'voxel_y': VoxelY,
    'voxel_z': VoxelZ,
    'euclidean_clusters': EuclideanClusters,
    # XYZ
    'custom_fit': CustomFit,
    'plane_fit': PlaneFit,
    'sphere_fit': SphereFit,
}
