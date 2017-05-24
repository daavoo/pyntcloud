import pandas as pd

from random import sample
from ..base import Sampling

class Sampling_Points(Sampling):
    """        
    """
    def __init__(self, pyntcloud):
        super().__init__(pyntcloud)
    
    def extract_info(self):
        self.points = self.pyntcloud.xyz
        
class RandomPoints(Sampling_Points):
    """ 'n' unique points randomly chosen

    Parameters
    ----------
    n: int
        Number of unique points that will be chosen.
    
    """
    def __init__(self, pyntcloud, n):
        super().__init__(pyntcloud)
        self.n = n
    
    def compute(self):
        #
        result = pd.DataFrame()

        result_xyz = self.points[sample(range(0, self.points.shape[0]), self.n)]
        
        result["x"] = result_xyz[:,0]
        result["y"] = result_xyz[:,1]
        result["z"] = result_xyz[:,2]
        
        #
        
        
        #return self.points[sample(range(0, self.points.shape[0]), self.n)]
        return result