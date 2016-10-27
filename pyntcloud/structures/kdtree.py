#  HAKUNA MATATA

"""
KDTree Class extending cKDTree
"""


from scipy.spatial import cKDTree

class KDTree(cKDTree):
    # TODO instead of extend cKDTree make this class a wrapper
    # around different KDTree implementations: scipy, flann, etc.

    def __init__(self, points, leafsize=16):
        super().__init__(points, leafsize=leafsize)
        self.id = "{}-{}".format("S", self.leafsize)
