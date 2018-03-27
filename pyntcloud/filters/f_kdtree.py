import numpy as np
from scipy.stats import zscore
from .base import Filter


class KDTreeFilter(Filter):

    def __init__(self, pyntcloud, kdtree_id):
        """
        Parameters
        ----------
        pyntcloud: pyntcloud.PyntCloud
        kdtree_id: string
            Usually returned from PyntCloud.add_structure("kdtree"):
            kdtree_id = my_cloud.add_structure("kdtree")
        """
        super().__init__(pyntcloud)
        self.kdtree_id = kdtree_id

    def extract_info(self):
        self.points = self.pyntcloud.xyz
        self.kdtree = self.pyntcloud.structures[self.kdtree]


class RadiousOutlierRemoval(KDTreeFilter):
    """Compute a Radious Outlier Removal filter using the given KDTree.

    Parameters
    ----------
    kdtree: pyntcloud.structures.KDTree
    k : int
        Number of neighbors that will be used to compute the filter.
    r : float
        The radius of the sphere with center on each point. The filter
        will look for the required number of neighboors inside that sphere.

    Notes
    -----
    > The distances between each point and his 'k' nearest neighbors that
        exceed the given 'r' are marked as False.

    > The points having any distance marked as False will be trimmed.

    The parameter r should be used in order to adjust the filter to
    the desired result.

    A LOWER 'r' value will result in a HIGHER number of points trimmed.
    """

    def __init__(self, pyntcloud, kdtree, k, r):
        super().__init__(pyntcloud, kdtree)
        self.k = k
        self.r = r

    def compute(self):
        distances = self.kdtree.query(self.points, k=self.k, n_jobs=-1)[0]
        ror_filter = np.all(distances < self.r, axis=1)

        return ror_filter


class StatisticalOutlierRemoval(KDTreeFilter):
    """Compute a Statistical Outlier Removal filter using the given KDTree.

    Parameters
    ----------
    kdtree: pyntcloud.structures.KDTree
    k : int
        Number of neighbors that will be used to compute the filter.
    z_max: float
        The maximum Z score wich determines if the point is an outlier.

    Notes
    -----
    > For each point, the mean of the distances between him and his 'k' nearest
        neighbors is computed.

    > The Z score of those means is computed.

    >  Points where the Z score is less than or more than 'z_max' are marked
        as False, in order to be trimmed.

    The optional parameter z_max should be used in order to adjust
    the filter to the desired result.

    A LOWER 'z_max' value will result in a HIGHER number of points trimmed.
    """

    def __init__(self, pyntcloud, kdtree, k, z_max):
        super().__init__(pyntcloud, kdtree)
        self.k = k
        self.z_max = z_max

    def compute(self):
        distances = self.kdtree.query(self.points, k=self.k, n_jobs=-1)[0]
        z_distances = zscore(np.mean(distances, axis=1), ddof=1)
        sor_filter = abs(z_distances) < self.z_max

        return sor_filter
