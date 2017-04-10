from scipy.spatial import cKDTree


class KDTree(cKDTree):

    def __init__(self, PyntCloud, leafsize=16):
        super().__init__(PyntCloud.xyz, leafsize=leafsize)
        self.id = "K({})".format(leafsize)
        self.PyntCloud = PyntCloud
    
    def extract_info(self):
        pass
    
    def compute(self):
        pass
    
    def get_and_set(self):
        
        self.PyntCloud.kdtrees[self.id] = self
        
        self.PyntCloud = None
        
        return self.id