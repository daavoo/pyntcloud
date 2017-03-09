import numpy as np
from .base import Sampling
from ..geometry.areas import triangle_area_multi

class Sampling_Mesh(Sampling):
    """        
    """
    def __init__(self, pyntcloud):
        super().__init__(pyntcloud)
    
    def extract_info(self):
        self.v1, self.v2, self.v3 = self.pyntcloud.get_mesh_vertices()

class RandomMeshSampling(Sampling_Mesh):
    """ Sample points adjusting probabilities according to triangle area.

    Parameters
    ----------
    n: int
        Number of points to be sampled
    """
    
    def __init__(self, pyntcloud, n):
        super().__init__(pyntcloud)
        self.n = n
        
    def compute(self):
        areas = triangle_area_multi(self.v1, self.v2, self.v3)
        probabilities = areas / np.sum(areas)
        random_idx = np.random.choice(np.arange(len(areas)), size=self.n, p=probabilities)
        
        v1 = self.v1[random_idx]
        v2 = self.v2[random_idx]
        v3 = self.v3[random_idx]
        
        # (n, 1) the 1 is for broadcasting
        u = np.random.rand(self.n, 1)
        v = np.random.rand(self.n, 1)
        is_a_problem = u + v > 1
        
        u[is_a_problem] = 1 - u[is_a_problem]
        v[is_a_problem] = 1 - v[is_a_problem]
        
        result = (v1 * u) + (v2 * v) + ((1 - (u + v)) * v3)
        
        return result