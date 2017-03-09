
"""
HAKUNA MATATA
"""

from .f_kdtree import (
    RadiousOutlierRemoval,
    StatisticalOutlierRemoval,
        
)
from .f_xyz import BoundingBox

ALL_FILTERS = {
    # XYZ     
    "BBOX": BoundingBox, 
    # KDTree        
    "ROR": RadiousOutlierRemoval,
    "SOR": StatisticalOutlierRemoval
}
