#  HAKUNA MATATA


from pandas import DataFrame

from .filters import (
    F_KDTREE,
    F_XYZ,
    ALL_FILTERS
)
from .io import FROM, TO
from .neighbors import k_neighbors, r_neighbors
from .plot import plot_points, DESCRIPTION
from .sampling import (
    S_POINTS,
    S_MESH,
    S_VOXELGRID,
    ALL_SAMPLING
)
from .scalar_fields import ( 
    SF_EIGENVALUES,
    SF_K_NEIGHBORS,
    SF_NORMALS,
    SF_RGB, 
    SF_VOXELGRID,
    SF_XYZ
)
from .structures import KDTree, VoxelGrid, Octree
from .utils.misc import crosscheck_kwargs_function


class PyntCloud(object):
    """ A Pythonic Point Cloud
    """
    
    def __init__(self, points, **kwargs):  
        self.points = points
        self.mesh = None
        for key in kwargs:
            if "kdtrees" in key:
                self.kdtrees = kwargs[key]
            elif "octrees" in key:
                self.octrees = kwargs[key]
            elif "voxelgrids" in key:
                self.voxelgrids = kwargs[key]
            else:
                setattr(self, key, kwargs[key])
        # store raw values to share memory along structures
        self.xyz = self.points[["x", "y", "z"]].values
        self.centroid = self.xyz.mean(0)

    def __repr__(self):
        default = [
            "_PyntCloud__points",
            "mesh",
            "kdtrees",
            "octrees",
            "voxelgrids",
            "centroid", 
            "xyz", 
            "filters"
        ]
        others = ["\n\t {}: {}".format(x, str(type(x))) for x in self.__dict__ if x not in default]
        
        if self.mesh is None:
            n_faces = 0
        else:
            n_faces = len(self.mesh)
            
        return DESCRIPTION.format(  
            len(self.points), len(self.points.columns) - 3,
            n_faces,
            len(self.kdtrees),
            len(self.octrees),
            len(self.voxelgrids),
            self.centroid[0], self.centroid[1], self.centroid[2],
            "".join(others))

    @property
    def points(self):
        return self.__points
    
    @points.setter
    def points(self, df):
        if not isinstance(df, DataFrame):
            raise TypeError("Points argument must be a DataFrame")
        elif not set(['x', 'y', 'z']).issubset(df.columns):
            raise ValueError("Points must have x, y and z coordinates")
        self._clean_all_structures()
        self.__points = df
             
    @classmethod
    def from_file(cls, filename):
        """ Extracts data from file and constructs a PyntCloud with it
        
        Parameters
        ----------
        filename : str
            Path to the file from wich the data will be readed

        Returns
        -------
        PyntCloud : object
            PyntCloud's instance, containing all valid elements in the file.
        """
        ext = filename.split(".")[-1].upper()
        if ext not in FROM:
            raise ValueError("Unsupported file format; supported formats are: {}".format(list(FROM)))       
        else:
            return cls(**FROM[ext](filename))

    def to_file(self, filename, internal=["points"], **kwargs):
        """ Save PyntCloud's data to file 

        Parameters
        ----------
        filename : str
            Path to the file from wich the data will be readed
            
        internals : list of str
        """
        
        ext = filename.split(".")[-1].upper()
        if ext not in TO:
            raise ValueError("Unsupported file format; supported formats are: {}".format(list(TO)))
        kwargs["filename"] = filename
        for x in internal:
            kwargs[x] = getattr(self, x)
        valid_args =  crosscheck_kwargs_function(kwargs, TO[ext])

        TO[ext](**valid_args)
        
    def add_scalar_field(self, name, **kwargs):
        """ Add one or multiple columns to PyntCloud.points

        Parameters
        ----------
        name : str
            One of the avaliable names in ALL_SF
        kwargs 
            Avaliable kwargs vary for each name.
        
        Returns
        -------
        sf_added : list of str
            The name of each of the columns (scalar fields) added.
            Usefull for chaining operations that require string names.
        
        Notes
        -----
        Avaliable scalar fields are:

        - REQUIRE EIGENVALUES
            KWARGS
                ev : list of str
                    Column names of the eigen values.
                    Tip: store in variable the return of self.add_scalar_field("eigen_values", ...)
            NAMES
                sphericity
                anisotropy
                linearity
                omnivariance
                eigenentropy
                planarity
                eigen_sum
                curvature

        - REQUIRE K_NEIGHBORS 
            KWARGS
                k_neighbors : (N, k) ndarray
                    Returned from self.get_neighbors(k, ...) or by manually querying some KDTree.                
            NAMES 
                eigen_decomposition
                eigen_values

        - REQUIRE NORMALS 
            KWARGS
                None
            NAMES 
                orientation_deg
                orientation_rad
                inclination_rad
                inclination_deg

        - REQUIRE RGB 
            KWARGS
                None
            NAMES 
                hsv
                relative_luminance
                rgb_intensity

        - REQUIRE VOXELGRID 
            KWARGS
                voxelgrid : VoxelGrid.id 
                    Tip: store in variable the return of self.add_structure("voxelgrid", ...)
            NAMES
                voxel_y
                voxel_x
                voxel_n
                voxel_z

        - REQUIRE XYZ
            KWARGS
                None
            AVALIABLE
                is_plane
                is_sphere

        """
        if name in SF_EIGENVALUES:
            k = kwargs["ev"][0].split("e1")[1]
            kwargs["ev"] = self.points[kwargs["ev"]].values
            valid_kwargs = crosscheck_kwargs_function(kwargs, SF_EIGENVALUES[name][1])
            all_sf = SF_EIGENVALUES[name][1](**valid_kwargs)
            sf_added = []
            for n, i in enumerate(SF_EIGENVALUES[name][0]):
                name = "{}{}".format(i, k)
                self.points[name] = all_sf[n].astype("f")
                sf_added.append(name)
        
        elif name in SF_K_NEIGHBORS:
            kwargs["k_neighbors"] = self.xyz[kwargs["k_neighbors"]]
            valid_kwargs = crosscheck_kwargs_function(kwargs, SF_K_NEIGHBORS[name][1])
            all_sf = SF_K_NEIGHBORS[name][1](**valid_kwargs)
            sf_added = []
            for n, i in enumerate(SF_K_NEIGHBORS[name][0]):
                name = "{}({})".format(i, valid_kwargs["k_neighbors"].shape[1])
                self.points[name] = all_sf[n].astype("f")
                sf_added.append(name)
        
        elif name in SF_NORMALS:
            kwargs["normals"] = self.points[["nx", "ny", "nz"]].values
            valid_kwargs = crosscheck_kwargs_function(kwargs, SF_NORMALS[name][1])
            all_sf = SF_NORMALS[name][1](**valid_kwargs)
            sf_added = []
            for n, i in enumerate(SF_NORMALS[name][0]):
                self.points[i] = all_sf[n]
                sf_added.append(i)

        elif name in SF_RGB:
            kwargs["rgb"] = self.points[["red", "green", "blue"]].values.astype("f")
            valid_kwargs = crosscheck_kwargs_function(kwargs, SF_RGB[name][1])
            all_sf = SF_RGB[name][1](**valid_kwargs)
            sf_added = []
            for n, i in enumerate(SF_RGB[name][0]):
                self.points[i] = all_sf[n]
                sf_added.append(i)

        elif name in SF_VOXELGRID:
            kwargs["voxelgrid"] = self.voxelgrids[kwargs["voxelgrid"]]
            valid_kwargs = crosscheck_kwargs_function(kwargs, SF_VOXELGRID[name][1])
            all_sf = SF_VOXELGRID[name][1](**valid_kwargs)
            sf_added = []
            for n, i in enumerate(SF_VOXELGRID[name][0]):
                name = "{}({})".format(i, valid_kwargs["voxelgrid"].id)
                self.points[name] = all_sf[n]
                sf_added.append(name)
        
        elif name in SF_XYZ:
            kwargs["points"] = self.xyz
            valid_kwargs = crosscheck_kwargs_function(kwargs, SF_XYZ[name][1])
            all_sf = SF_XYZ[name][1](**valid_kwargs)
            sf_added = []
            for n, i in enumerate(SF_XYZ[name][0]):
                self.points[i] = all_sf[n]
                sf_added.append(i)

        else:
            raise ValueError("Unsupported scalar field. Check docstring")

        return sf_added

    def add_structure(self, name, **kwargs):
        """ Build a structure and add it to the corresponding PyntCloud's attribute
        """
        kwargs["points"] = self.xyz
        structures = {
            'kdtree':(KDTree, self.kdtrees),
            'voxelgrid':(VoxelGrid, self.voxelgrids), 
            'octree':(Octree, self.octrees)
            }
        if name in structures:
            valid_kwargs = crosscheck_kwargs_function(kwargs, structures[name][0])  
            structure = structures[name][0](**valid_kwargs)
            structures[name][1][structure.id] = structure
        else:
            raise ValueError("Unsupported structure; supported structures are: {}".format(list(structures)))
            
        return structure.id 

    def get_filter(self, name, **kwargs):
        """ Compute filter over PyntCloud's points and return it
        """
        kwargs["points"] = self.xyz
        
        if name in F_XYZ:
            valid_args = crosscheck_kwargs_function(kwargs, F_XYZ[name])
            return F_XYZ[name](**valid_args)

        elif name in F_KDTREE:
            kwargs["kdtree"] = self.kdtrees[kwargs["kdtree"]]
            valid_args = crosscheck_kwargs_function(kwargs, F_KDTREE[name])
            return F_KDTREE[name](**valid_args)

        else:
            raise ValueError("Unsupported filter; supported filters are: {}".format(ALL_FILTERS)) 
    
    def get_sample(self, name, **kwargs):
        """ Returns arbitrary number of points sampled by selected method
        """
        if name in S_POINTS:
            kwargs["points"] = self.xyz
            valid_args = crosscheck_kwargs_function(kwargs, S_POINTS[name])
            return S_POINTS[name](**valid_args)
        
        elif name in S_MESH:
            kwargs["v1"], kwargs["v2"], kwargs["v3"] = self.get_mesh_vertices()
            valid_args = crosscheck_kwargs_function(kwargs, S_MESH[name])
            return S_MESH[name](**valid_args)
        
        elif name in S_VOXELGRID:
            kwargs["voxelgrid"] = self.voxelgrids[kwargs["voxelgrid"]]
            valid_args = crosscheck_kwargs_function(kwargs, S_VOXELGRID[name])
            return S_VOXELGRID[name](**valid_args)
        
        else:
            raise ValueError("Unsupported sample mode; supported modes are: {}".format(ALL_SAMPLING))
    
    def get_neighbors(self, k=None, r=None, kdtree=None):
        """ For each point finds the indices that compose it's neighbourhood.

        Parameters
        ----------
        k : int, Default None
            For "K-nearest neighbor" search.
            Number of nearest neighbors that will be used to build the neighbourhood.

        r : float, Default None
            For "Fixed-radius near neighbors" search.
            Radius of the sphere that will be used to build the neighbourhood.

        kdtree : str, Default None
            KDTree.id in self.kdtrees.

            If kdtree is None and k is not None:
                The KDTree will be computed and added to PyntCloud as part of the process.
            Elif r is not None:
                kdtree kwarg will be ignored.
            Else:
                The given KDTree will be used for "K-nearest neighbor" search.

        Returns
        -------
        neighbors : array-like
            (N, k) ndarray if k is not None.                
                Indices of the 'k' nearest neighbors for the 'N' points.
            (N,) ndarray of lists if r is not None.
                Array holding a variable number of indices corresponding
                to the neighbors with distance < r.
        """
        if k is not None:
            if kdtree is None:
                kdtree_id = self.add_structure("kdtree")
                kdtree = self.kdtrees[kdtree_id]
            else:
                kdtree = self.kdtrees[kdtree]

            return k_neighbors(self.xyz, k, kdtree)

        elif r is not None:
            return r_neighbors(self.xyz, r)
        else:
            raise ValueError("You must supply 'k' or 'r' values.")
        
    def get_mesh_vertices(self):
        """ Decompose triangles of self.mesh from vertices in self.points
        Returns
        -------
        v1, v2, v3: ndarray
            (N, 3) arrays of vertices so v1[i], v2[i], v3[i] represent the ith triangle
        """
        
        v1 = self.xyz[[self.mesh["v1"]]]
        v2 = self.xyz[[self.mesh["v2"]]]
        v3 = self.xyz[[self.mesh["v3"]]]

        return v1, v2, v3
        
    def _clean_all_structures(self):
        self.mesh = None
        self.kdtrees = {}
        self.voxelgrids = {}
        self.octrees = {}


    
