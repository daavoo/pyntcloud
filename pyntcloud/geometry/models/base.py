from abc import ABC, abstractmethod


class GeometryModel(ABC):

    @abstractmethod
    def from_k_points(self):
        pass

    @abstractmethod
    def get_projections(self):
        pass
