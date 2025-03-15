"""
HAKUNA MATATA
"""

from .fitters import single_fit
from .models import RansacPlane, RansacSphere
from .samplers import RandomRansacSampler, VoxelgridRansacSampler

RANSAC_MODELS = {"plane": RansacPlane, "sphere": RansacSphere}
RANSAC_SAMPLERS = {"random": RandomRansacSampler, "voxelgrid": VoxelgridRansacSampler}

__all__ = ["single_fit", "RANSAC_MODELS", "RANSAC_SAMPLERS"]
