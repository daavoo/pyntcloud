from abc import ABC, abstractmethod
from collections import OrderedDict

class ScalarField(ABC):
    """ Base class for scalar fields.
    """

    def __init__(self, pyntcloud):
        self.pyntcloud = pyntcloud
        self.to_be_added = OrderedDict()
    
    def get_and_set(self):
        sf_added = []
        for k, v in self.to_be_added.items():
            sf_added.append(k)
            self.pyntcloud.points[k] = v
        return sf_added

    @abstractmethod
    def extract_info(self):
        pass
    
    @abstractmethod
    def compute(self):
        pass
    
    
