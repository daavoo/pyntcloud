
"""
HAKUNA MATATA
"""

from .kdtree import (
    RadiusOutlierRemovalFilter,
    StatisticalOutlierRemoval,

)
from .f_xyz import BoundingBox

ALL_FILTERS = {
    # XYZ
    "BBOX": BoundingBox,
    # KDTree
    "ROR": RadiusOutlierRemovalFilter,
    "SOR": StatisticalOutlierRemoval
}
