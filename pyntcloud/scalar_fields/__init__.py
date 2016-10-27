
"""
HAKUNA MATATA
"""

from .scalar_fields import *

NEED_NORMALS = {
'inclination_deg': 'inclination_deg',
'inclination_rad': 'inclination_rad',
'orientation_deg': 'orientation_deg',
'orientation_rad': 'orientation_rad',
}

NEED_RGB = {
'rgb_intensity' : ['Ri', 'Gi', 'Bi'],
'relative_luminance': 'relative_luminance',
'hsv' : ['H', 'S', 'V']
}

NEED_NEIGHBOURHOOD = {
'eigen_decomposition' : ['eigval_1', 'eigval_2', 'eigval_3', 'eigvec_1', 'eigvec_2', 'eigvec_3']
}


