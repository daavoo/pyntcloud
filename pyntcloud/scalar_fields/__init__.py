
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
'eigen_values': ['e_1', 'e_2', 'e_3'],
'eigen_sum': 'eigen_sum',
'omnivariance': 'omnivariance',
'eigenentropy': 'eigenentropy',
'anisotropy': 'anisotropy',
'planarity': 'planarity',
'linearity': 'linearity',
'curvature': 'curvature',
'sphericity': 'sphericity',
'verticality':'verticality'
}

ALL_SF = "  ".join(NEED_NORMALS.keys()) + " "\
        "  ".join(NEED_RGB.keys()) + " "\
        "  ".join(NEED_NEIGHBOURHOOD.keys())


