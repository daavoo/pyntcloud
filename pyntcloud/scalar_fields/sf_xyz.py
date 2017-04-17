import numpy as np
from ..ransac import single_fit, RANSAC_MODELS, RANSAC_SAMPLERS
from ..base import ScalarField

class ScalarField_XYZ(ScalarField):
    """
    Parameters
    ----------
    model : ransac.model.RansacModel
        Model that will be fitted to points
    
    sampler : ransac.sampler.RansacSampler
        Sampler function that will be used when fitting the model.
    """
    def __init__(self, pyntcloud):
        super().__init__(pyntcloud)   
    
    def extract_info(self):
        self.points = self.pyntcloud.xyz
    
       
class PlaneFit(ScalarField_XYZ):
    """ Points belonging to the best RansacPlane found.
    """
    def __init__(self, pyntcloud, max_dist=1e-4, max_iterations=100, n_inliers_to_stop=None):
        self.model = RANSAC_MODELS["plane"]
        self.sampler = RANSAC_SAMPLERS["random"]
        self.name = "is_plane"
        self.model_kwargs = {"max_dist" : max_dist}
        self.max_iterations = max_iterations
        self.n_inliers_to_stop = n_inliers_to_stop
        
        super().__init__(pyntcloud)
        
    def compute(self):
        self.to_be_added[self.name] =  single_fit(self.points, self.model, self.sampler,
                                         model_kwargs=self.model_kwargs,
                                         max_iterations=self.max_iterations,
                                         n_inliers_to_stop=self.n_inliers_to_stop).astype(np.uint8)

class SphereFit(ScalarField_XYZ):
    """ Returns wich points belong to the best RansacSphere found.

    """
    def __init__(self, pyntcloud, max_dist=1e-4, max_iterations=100, n_inliers_to_stop=None):
        self.model = RANSAC_MODELS["sphere"]
        self.sampler = RANSAC_SAMPLERS["random"]
        self.name = "is_sphere"
        self.model_kwargs = {"max_dist" : max_dist}
        self.max_iterations = max_iterations
        self.n_inliers_to_stop = n_inliers_to_stop
        
        super().__init__(pyntcloud)
        
    def compute(self):
        self.to_be_added[self.name] =  single_fit(self.points, self.model, self.sampler,
                                         model_kwargs=self.model_kwargs,
                                         max_iterations=self.max_iterations,
                                         n_inliers_to_stop=self.n_inliers_to_stop).astype(np.uint8)

class CustomFit(ScalarField_XYZ):
    """ Fit using custom model and/or sampler
    """
    
    def __init__(self, pyntcloud, model, sampler, name, model_kwargs={}, sampler_kwargs={}, max_iterations=100):
        self.model = model
        self.sampler = sampler
        self.name = name
        self.model_kwargs = model_kwargs
        self.sampler_kwargs = sampler_kwargs
        self.max_iterations = max_iterations
        super().__init__(pyntcloud)
        
    def compute(self):
        self.to_be_added[self.name] =  single_fit(self.points, self.model,self.sampler,
                                         model_kwargs=self.model_kwargs,
                                         sampler_kwargs=self.sampler_kwargs,
                                         max_iterations=self.max_iterations)
