from scipy.spatial import cKDTree

from ..base import Structure


class KDTree(cKDTree, Structure):

    def __init__(self, PyntCloud, leafsize=16):
        cKDTree.__init__(self, PyntCloud.xyz, leafsize=leafsize)
        Structure.__init__(self, PyntCloud)
        self.id = "K({})".format(leafsize)
        self.PyntCloud = PyntCloud

    def extract_info(self):
        pass

    def compute(self):
        pass
