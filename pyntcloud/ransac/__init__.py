
"""
HAKUNA MATATA
"""
    
from .fitters import single_fit
from .models import RansacPlane, RansacSphere
from .samplers import RandomSampler, VoxelgridSampler

RANSAC_MODELS = {
    "plane" : RansacPlane,
    "sphere" : RansacSphere
}
RANSAC_SAMPLERS = {
    "random" : RandomSampler,
    "voxelgrid" : VoxelgridSampler
}