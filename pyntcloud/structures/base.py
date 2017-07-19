from abc import ABC, abstractmethod


class Structure(ABC):
    """Base class for structures."""

    def __init__(self, PyntCloud):
        self.PyntCloud = PyntCloud

    def get_and_set(self):
        self.PyntCloud.structures[self.id] = self
        return self.id

    @abstractmethod
    def extract_info(self):
        pass

    @abstractmethod
    def compute(self):
        pass


class StructuresDict(dict):
    """Custom class to restrict PyntCloud.structures assigment."""

    def __init__(self, *args):
        self.n_voxelgrids = 0
        self.n_kdtrees = 0
        self.n_delanuays = 0
        self.n_convex_hulls = 0
        super().__init__(*args)

    def __setitem__(self, key, val):
        if not issubclass(val.__class__, Structure):
            raise TypeError("{} must be base.Structure subclass".format(key))

        # TODO better structure.id check
        if key.startswith("V"):
            self.n_voxelgrids += 1
        elif key.startswith("K"):
            self.n_kdtrees += 1
        elif key.startswith("D"):
            self.n_delanuays += 1
        elif key.startswith("CH"):
            self.n_convex_hulls += 1
        else:
            raise ValueError("{} is not a valid structure.id".format(key))
        super().__setitem__(key, val)
