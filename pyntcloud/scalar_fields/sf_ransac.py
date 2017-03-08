from ..ransac import single_fit, RANSAC_MODELS, RANSAC_SAMPLERS
from .base import ScalarField

class ScalarField_Ransac(ScalarField):
    """
    Parameters
    ----------
    model : ransac.model.RansacModel
        Model that will be fitted to points
    
    sampler : ransac.sampler.RansacSampler
        Sampler function that will be used when fitting the model.
    """
    def __init__(self, pyntcloud, model, sampler, model_kwargs={}, sampler_kwargs={}, max_iterations=100):
        super().__init__(pyntcloud)
        self.model = model
        self.sampler = sampler
        self.model_kwargs = model_kwargs
        self.sampler_kwargs = sampler_kwargs
        self.max_iterations = max_iterations        
    
    def extract_info(self):
        self.points = self.pyntcloud.xyz
    
    def compute(self):
        self.to_be_added[self.name] =  single_fit(self.model, self.sampler,
                                         model_kwargs=self.model_kwargs,
                                         sampler_kwargs=self.sampler_kwargs,
                                         max_iterations=self.max_iterations)
        
class PlaneFit(ScalarField_Ransac):
    """ Points belonging to the best RansacPlane found.
    """
    def __init__(self, pyntcloud, max_dist=1e-4, max_iterations=100):
        model = RANSAC_MODELS["plane"]
        sampler = RANSAC_SAMPLERS["random"]
        self.name = "is_plane"
        model_kwargs = {"max_dist" : max_dist}
        super().__init__(pyntcloud, model, sampler, model_kwargs=model_kwargs, max_iterations=max_iterations)
        

class SphereFit(ScalarField_Ransac):
    """ Returns wich points belong to the best RansacSphere found.

    """
    def __init__(self, pyntcloud, max_dist=1e-4,  max_iterations=100):
        model = RANSAC_MODELS["sphere"]
        sampler = RANSAC_SAMPLERS["random"]
        self.name = "is_sphere"
        model_kwargs = {"max_dist" : max_dist}
        super().__init__(pyntcloud, model, sampler, model_kwargs=model_kwargs, max_iterations=max_iterations)
        

class CustomFit(ScalarField_Ransac):
    """ Fit using custom model and/or sampler
    """
    
    def __init__(self, pyntcloud, model, sampler, name, model_kwargs={}, sampler_kwargs={}, max_iterations=100):
        super().__init__(pyntcloud, model, sampler model_kwargs=model_kwargs, sampler_kwargs=sampler_kwargs, max_iterations=max_iterations)
        self.name = name