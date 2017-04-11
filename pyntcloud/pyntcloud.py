#  HAKUNA MATATA

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from .filters import ALL_FILTERS
from .io import FROM, TO
from .neighbors import k_neighbors, r_neighbors
from .plot import DESCRIPTION, plot_PyntCloud
from .sampling import ALL_SAMPLING
from .scalar_fields import ALL_SF
from .structures import ALL_STRUCTURES
from .utils.misc import crosscheck_kwargs_function


class PyntCloud(object):
    """ A Pythonic Point Cloud

    Parameters
    ----------
    points : pd.DataFrame
        Core component. 
        DataFrame of N rows by M columns.
        Each row represents one point of the point cloud.
        Each column represents one scalar field associated to it's corresponding point.
        
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
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Points argument must be a DataFrame")
        elif not set(['x', 'y', 'z']).issubset(df.columns):
            raise ValueError("Points must have x, y and z coordinates")
        self._clean_all_structures()
        self.__points = df
        self.xyz = self.__points[["x", "y", "z"]].values
             
    @classmethod
    def from_file(cls, filename):
        """ Extracts data from file and constructs a PyntCloud with it
        
        Parameters
        ----------
        filename: str
            Path to the file from wich the data will be readed

        Returns
        -------
        PyntCloud: object
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
        filename: str
            Path to the file from wich the data will be readed
            
        internals: list of str, optional
            Default: ["points"]
            Names of the attributes that will be extracted from the PyntCloud.
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
        name: str
            One of the avaliable names. See bellow.
        kwargs 
            Vary for each name. See bellow.
        
        Returns
        -------
        sf_added: list of str
            The name of each of the columns (scalar fields) added.
            Usefull for chaining operations that require string names.
        
        Notes
        -----
        
        Avaliable scalar fields are:

        **REQUIRE EIGENVALUES**

            ARGS
                ev: list of str
                    ev = self.add_scalar_field("eigen_values", ...)

            sphericity
            
            anisotropy
            
            linearity
            
            omnivariance
            
            eigenentropy
            
            planarity
            
            eigen_sum
            
            curvature
                
        **REQUIRE K_NEIGHBORS** 

            ARGS
                k_neighbors: (N, k) ndarray
                    Returned from: self.get_neighbors(k, ...) / manually querying some self.kdtrees[x] / other methods.                

            eigen_decomposition
            
            eigen_values
            
        **REQUIRE NORMALS**

            orientation_deg
            
            orientation_rad
            
            inclination_rad
            
            inclination_deg
                
        **REQUIRE RGB**

            hsv
            
            relative_luminance
            
            rgb_intensity
                

        **REQUIRE VOXELGRID**

            ARGS
                voxelgrid: VoxelGrid.id
                    voxelgrid = self.add_structure("voxelgrid", ...)
                     
            voxel_x
            
            voxel_y
            
            voxel_n
            
            voxel_z
            
            euclidean_clusters
                

        **ONLY REQUIRE XYZ**

            plane_fit
                max_dist: float, optional 
                    Default: 1e-4
                    Maximum distance from point to model in order to be considered as inlier.
                max_iterations: int, optional (Default 100)
                    Maximum number of fitting iterations.
                    
            sphere_fit
                max_dist: float, optional 
                    Default: 1e-4
                    Maximum distance from point to model in order to be considered as inlier.
                max_iterations: int, optional 
                    Default: 100
                    Maximum number of fitting iterations.
                    
            custom_fit
                model: subclass of ransac.models.RansacModel
                    Model to be fitted
                sampler: subclass of ransac.models.RansacSampler
                    Sample method to be used
                name: str
                    Will be used to name the added column
                model_kwargs: dict, optional 
                    Default: {}
                    Will be passed to single_fit function.
                sampler_kwargs: dict, optional 
                    Default: {}
                    Will be passed to single_fit function.
        """
        
        if name in ALL_SF:
            SF = ALL_SF[name](self, **kwargs)
            SF.extract_info()
            SF.compute()
            sf_added = SF.get_and_set()

        else:
            raise ValueError("Unsupported scalar field. Check docstring")

        return sf_added

    def add_structure(self, name, **kwargs):
        """ Build a structure and add it to the corresponding PyntCloud's attribute
        
        Parameters
        ----------
        name: str
            One of the avaliable names. See bellow.
        kwargs 
            Vary for each name. See bellow.
        
        Returns
        -------
        structure.id: str
            Identification string associated with the added structure.
            Usefull for chaining operations that require string names.
        
        Notes
        -----
        Avaliable structures are:
        
        **ONLY REQUIRE XYZ**

            kdtree
                leafsize: int, optional
                    Default: 16
                    The number of points at which the algorithm switches over to brute-force. 
                    Has to be positive.
    
            voxelgrid 
                x_y_z: list of int, optional
                    Default: [2, 2, 2]
                    The number of segments in wich each axis will be divided.
                    x_y_z[0]: x axis 
                    x_y_z[1]: y axis 
                    x_y_z[2]: z axis
                    If sizes is not None it will be ignored.
                sizes: list of float, optional
                    Default: None
                    The desired voxel size along each axis.
                    sizes[0]: voxel size along x axis.
                    sizes[1]: voxel size along y axis.
                    sizes[2]: voxel size along z axis.
                bb_cuboid: bool, optional
                    Default: True
                    If True, the bounding box of the point cloud will be adjusted
                    in order to have all the dimensions of equal lenght. 
    
            octree
                TODO
        
        """
        if name in ALL_STRUCTURES:
            STRUCTURE = ALL_STRUCTURES[name](self, **kwargs)
            STRUCTURE.extract_info()
            STRUCTURE.compute()
            added = STRUCTURE.get_and_set()

        else:
            raise ValueError("Unsupported scalar field. Check docstring")

        return added

    def get_filter(self, name, **kwargs):
        """ Compute filter over PyntCloud's points and return it
        
        Parameters
        ----------
        name: str
            One of the avaliable names. See bellow.
            
        kwargs 
            Vary for each name. See bellow.
        
        Returns
        -------
        filter: boolean array
            Boolean mask indicating wherever a point should be keeped or not.
            The size of the boolean mask will be the same as the number of points
            in the pyntcloud.
        
        Notes
        -----
        
        Avaliable filters are:

        **REQUIRE KDTREE**
        
            ARGS
                kdtree : KDTree.id
                    kdtree = self.add_structure("kdtree", ...)
            
            ROR    (Radius Outlier Removal)
                k: int
                    Number of neighbors that will be used to compute the filter.                                  
                r: float
                    The radius of the sphere with center on each point. The filter
                    will look for the required number of neighboors inside that sphere. 
                    
            SOR    (Statistical Outlier Removal)
                k: int
                    Number of neighbors that will be used to compute the filter. 
                z_max: float
                    The maximum Z score wich determines if the point is an outlier.
                    
        **ONLY REQUIRE XYZ**

            BBOX    (Bounding Box)
                min_i, max_i: float
                    The bounding box limits for each coordinate. If some limits are missing,
                    the default values are -infinite for the min_i and infinite for the max_i.    
                
        """

        if name in ALL_FILTERS:
            F = ALL_FILTERS[name](self, **kwargs)
            F.extract_info()
            return F.compute()

        else:
            raise ValueError("Unsupported filter. Check docstring")
            
    def get_sample(self, name, **kwargs):
        """ Returns arbitrary number of points sampled by selected method
        
        Parameters
        ----------
        name: str
            One of the avaliable names. 
            See bellow.
            
        kwargs 
            Vary for each name. 
            See bellow.
        
        Returns
        -------
        sampled_points: (n, 3) ndarray
            'n' vary for each method.
            
        Notes
        -----
        
        Avaliable sampling methods are:
            
        **REQUIRE MESH**
        
            mesh_random_sampling
                n: int
                    Number of points to be sampled. 
                rgb: bool, optional
                    Default: False
                    Indicates if rgb values will be also sampled
                normals: bool, optional
                    Default: False
                    Indicates if normals will be also sampled
                    
        **REQUIRE VOXELGRID**
        
            ARGS
                voxelgrid: VoxelGrid.id
                    voxelgrid = self.add_structure("voxelgrid", ...)
            
            voxelgrid_centers    
             
            voxelgrid_centroids
            
            voxelgrid_nearest    

        
        **USE POINTS**
        
            points_random_sampling
                n: int    
                    Number of points to be sampled.                      

        """
        if name in ALL_SAMPLING:
            S = ALL_SAMPLING[name](self, **kwargs)
            S.extract_info()
            return S.compute()

        else:
            raise ValueError("Unsupported sampling. Check docstring") 
            
    def get_neighbors(self, k=None, r=None, kdtree=None):
        """ For each point finds the indices that compose it's neighbourhood.

        Parameters
        ----------
        k: int, optional
            Default: None
            For "K-nearest neighbor" search.
            Number of nearest neighbors that will be used to build the neighbourhood.

        r: float, optional
            Default: None
            For "Fixed-radius neighbors" search.
            Radius of the sphere that will be used to build the neighbourhood.

        kdtree: str, optional
            Default: None
            KDTree.id in self.kdtrees.
            
            - If **kdtree** is None and **k** is not None:
                
            The KDTree will be computed and added to PyntCloud as part of the process.
            
            - Elif **r** is not None:
                
            kdtree kwarg will be ignored.
            
            - Else:
                
            The given KDTree will be used for "K-nearest neighbor" search.

        Returns
        -------
        neighbors: array-like
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
            return k_neighbors(kdtree, k)
        
        elif r is not None:
            return r_neighbors(self.xyz, r)
        else:
            raise ValueError("You must supply 'k' or 'r' values.")
        
    def get_mesh_vertices(self, rgb=False, normals=False):
        """ Decompose triangles of self.mesh from vertices in self.points
        
        Returns
        -------
        v1, v2, v3: ndarray
            (N, 3) arrays of vertices so v1[i], v2[i], v3[i] represent the ith triangle
        """
        
        use_columns = ["x", "y", "z"]
        if rgb:
            use_columns.extend(["red", "green", "blue"])
        if normals:
            use_columns.extend(["nx","ny","nz"])
        
        points = self.points[use_columns].values
        
        v1 = points[[self.mesh["v1"]]]
        v2 = points[[self.mesh["v2"]]]
        v3 = points[[self.mesh["v3"]]]

        return v1, v2, v3
        
    def _clean_all_structures(self):
        """ Utility function. Implicity called when self.points is assigned.
        """
        self.mesh = None
        self.kdtrees = {}
        self.voxelgrids = {}
        self.octrees = {}
        
        
    def plot(self, 
             use_as_color=["red", "green", "blue"], 
             cmap="hsv",
             output_name="pyntcloud_plot",
             width=800,
             height=500):
        """ Visualize PyntCloud in a Jupyter notebook using three.js
        
        Parameters
        ----------
        use_as_color: str or ["red", "green", "blue"], optional
            Default: ["red", "green", "blue"]
            Indicates wich scalar fields will be used to colorize the rendered
            point cloud.
        
        cmap: str, optional
            Default: "hsv"
            Color map that will be used to convert a single scalar field into rgb.
            Check matplotlib cmaps.
        
        output_name: str, optional
            Default: "pyntcloud_plot"
            Base filename that will be used to create:
                output_name.html
                output_name.ply
                output_name.json
                
        width: int, optional
            Default: 800
            Adjusts the size of the IFrame plotted in Jupyter notebook.
        
        height: int, optional
            Default: 500
            Adjusts the size of the IFrame plotted in Jupyter notebook.
            
        Returns
        -------
        Ipython.display.IFrame
            output_name.html inside an IFrame
        
        Notes
        ----- 
        You can visualize the output_name.html outside the notebook as a regular
        html. You might need to run a local server or adjust the browser privacy
        policies in order to allow javascript to load local files.
        
        """
        
        try:
            colors = self.points[use_as_color].values
        except:
            colors = None
        
        if use_as_color != ["red", "green", "blue"] and colors is not None:
            s_m = plt.cm.ScalarMappable(cmap=cmap)
            colors = s_m.to_rgba(colors)[:,:-1]   * 255
        
        elif colors is None:
            # default color orange
            colors = np.repeat([[255,125,0]], self.xyz.shape[0], axis=0)
        
        colors = colors.astype(np.uint8)
        
        points = pd.DataFrame(self.xyz, columns=["x","y","z"])
        
        for n, i in enumerate(["red", "green", "blue"]):
            points[i] = colors[:,n]
        
        new_PyntCloud = PyntCloud(points)

        return plot_PyntCloud(new_PyntCloud, output_name=output_name)

    
