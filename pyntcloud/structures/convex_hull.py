import pandas as pd
from scipy.spatial import ConvexHull as scipy_ConvexHull
from itertools import combinations

from .base import Structure


class ConvexHull(scipy_ConvexHull, Structure):

    def __init__(self, PyntCloud,
                 incremental=False,
                 qhull_options=None):
        Structure.__init__(self, PyntCloud)
        self._incremental = incremental
        self._qhull_options = qhull_options

    def extract_info(self):
        """ABC API"""
        self._points = self.PyntCloud.xyz
        self.id = "CH({})".format(self._qhull_options)

    def compute(self):
        """ABC API"""
        scipy_ConvexHull.__init__(self,
                                  self._points,
                                  self._incremental,
                                  self._qhull_options)

    def get_mesh(self):
        """
        Use convex hull simplices to build mesh.

        The returned mesh is in mesh-vertex format, suitable for
        been assigned to PyntCloud.mesh.
        """
        mesh = pd.DataFrame(self.simplices, columns=["v1", "v2", "v3"])

        return mesh
