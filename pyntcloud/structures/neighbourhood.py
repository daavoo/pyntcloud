#  HAKUNA MATATA

"""
Neighbourhood Class
"""

class Neighbourhood(object):
    
    def __init__(self, kdtree, k, **kwargs):
        """
        Parameters
        ----------         
        """
        self.k = k
        self.id = "{}-{}".format(kdtree.id, self.k)

        d, i = kdtree.query(kdtree.data, k=k, n_jobs=-1, **kwargs)
        # discard self neighbour with [:,1:]
        self.distances = d[:,1:]
        self.indices = i[:,1:]
        

