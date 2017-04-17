""" Abstract Base Classes API
"""
from abc import ABC, abstractmethod
from collections import OrderedDict

# filters ---------------------------------------------------------------------

class Filter(ABC):
    """ Base class for filters.
    """

    def __init__(self, pyntcloud):
        self.pyntcloud = pyntcloud

    @abstractmethod
    def extract_info(self):
        pass
    
    @abstractmethod
    def compute(self):
        pass
    
# sampling --------------------------------------------------------------------

class Sampling(ABC):
    """ Base class for sampling methods.
    """

    def __init__(self, pyntcloud):
        self.pyntcloud = pyntcloud

    @abstractmethod
    def extract_info(self):
        pass
    
    @abstractmethod
    def compute(self):
        pass
    
# scalar_fields ---------------------------------------------------------------

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
        
        if len(sf_added) == 1:
            return sf_added[0]
        else:
            return sf_added

    @abstractmethod
    def extract_info(self):
        pass
    
    @abstractmethod
    def compute(self):
        pass

# structures ------------------------------------------------------------------
 
class Structure(ABC):
    """ Base class for scalar fields.
    """

    def __init__(self, PyntCloud):
        self.PyntCloud = PyntCloud
    
    @abstractmethod
    def extract_info(self):
        pass
    
    @abstractmethod
    def compute(self):
        pass
    
    @abstractmethod
    def get_and_set(self):
        pass
    
    @abstractmethod
    def query(self):
        pass