#  HAKUNA MATATA

"""
Neighbourhood Class
"""

class Neighbourhood(object):
    
    def __init__(self, n, k, d, i):
        """
        Parameters
        ----------         
        n: int 
            Indicates wich KDTree was used to generate the Neighbourhood. 
            "n"" is the index in the PyntCloud.kdtrees list.
        
        k: int 
            Number of neighbours.
        
        d: ndarray
            Distances returned from KDTree.query
        i: ndarray
            Indices returned from KDTree.query
        """
        self.n = n
        self.k = k
        self.id = "n:{} k:{}".format(self.n, self.k)
        self.distances = d
        self.indices = i

