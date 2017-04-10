from abc import ABC, abstractmethod

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
