from .base import Structure

from scipy.spatial import cKDTree


class KDTree(Structure, cKDTree):

    def __init__(self, PyntCloud, leafsize=16):
        Structure.__init__(self, PyntCloud)
        cKDTree.__init__(self, self.PyntCloud.xyz, leafsize=leafsize)
        self.id = "K({})".format(leafsize)
    
    def extract_info(self):
        return
        
    def compute(self):
        return
    
    def query(self):
        return
    
    def get_and_set(self):
        
        self.PyntCloud.kdtrees[self.id] = self
        
        self.PyntCloud = None
        
        return self.id