#  HAKUNA MATATA


import numpy as np
import pandas as pd

from inspect import signature
from matplotlib import pyplot as plt

from .io import *
from .plot import *
from .scalar_fields import *
from .structures import *


### __repr__ method
DESCRIPTION = """\
PyntCloud
=========\n
{} points with {} scalar fields
{} faces in mesh
{} kdtrees
{} neighbourhoods
{} octrees
{} voxelgrids\n
Centroid: {}, {}, {}\n
Other attributes:{}        
"""

### Constant Exceptions
MUST_HAVE_POINTS = ValueError("There must be a 'points' key in the kwargs")
MUST_HAVE_XYZ = ValueError("Points must have x, y and z coordinates")
UNSOPORTED_IN = ValueError("Unsupported file format; supported formats are: "  + "  ".join(FORMATS_READERS.keys()))
UNSOPORTED_OUT = ValueError("Unsupported file format; supported formats are: "  + "  ".join(FORMATS_WRITERS.keys()))
UNSOPORTED_SF = ValueError("Unsupported scalar field; supported scalar fields are: "  + "  ".join(NEED_NORMALS.keys()) 
                            +"  ".join(NEED_RGB.keys()) +"  ".join(NEED_NEIGHBOURHOOD.keys()) )
UNSOPORTED_STRUCTURE = ValueError("Unsupported structure; supported structures are: 'kdtree', 'voxelgrid', 'neighbourhood'")
MUST_BE_DF = TypeError("Points argument is not a DataFrame")



"""                                                                                                         
,-.----.                                                                                                     
\    /  \                                ___       ,----..     ,--,                                          
|   :    \                             ,--.'|_    /   /   \  ,--.'|                                    ,---, 
|   |  .\ :                   ,---,    |  | :,'  |   :     : |  | :       ,---.            ,--,      ,---.'| 
.   :  |: |               ,-+-. /  |   :  : ' :  .   |  ;. / :  : '      '   ,'\         ,'_ /|      |   | : 
|   |   \ :       .--,   ,--.'|'   | .;__,'  /   .   ; /--`  |  ' |     /   /   |   .--. |  | :      |   | | 
|   : .   /     /_ ./|  |   |  ,"' | |  |   |    ;   | ;     '  | |    .   ; ,. : ,'_ /| :  . |    ,--.__| | 
;   | |`-'   , ' , ' :  |   | /  | | :__,'| :    |   : |     |  | :    '   | |: : |  ' | |  . .   /   ,'   | 
|   | ;     /___/ \: |  |   | |  | |   '  : |__  .   | '___  '  : |__  '   | .; : |  | ' |  | |  .   '  /  | 
:   ' |      .  \  ' |  |   | |  |/    |  | '.'| '   ; : .'| |  | '.'| |   :    | :  | : ;  ; |  '   ; |:  | 
:   : :       \  ;   :  |   | |--'     ;  :    ; '   | '/  : ;  :    ;  \   \  /  '  :  `--'   \ |   | '/  ' 
|   | :        \  \  ;  |   |/         |  ,   /  |   :    /  |  ,   /    `----'   :  ,      .-./ |   :    :| 
`---'.|         :  \  \ '---'           ---`-'    \   \ .'    ---`-'               `--`----'      \   \  /   
  `---`          \  ' ;                            `---`                                           `----'    
                  `--`                                                                                                                                                                                                                                                                                                                                                                    
"""

class PyntCloud(object):
    """ A Pythonic Point Cloud
    """
    
    def __init__(self, **kwargs):  

        if "points" not in kwargs:
            raise MUST_HAVE_POINTS
        
        self.kdtrees = {}
        self.neighbourhoods= {}
        self.octrees = {}
        self.voxelgrids = {}

        for key in kwargs:
            if "kdtrees" in key:
                self.kdtrees = kwargs[key]
            elif "neighbourhoods" in key:
                self.neighbourhoods = kwargs[key]
            elif "octrees" in key:
                self.octrees = kwargs[key]
            elif "voxelgrids" in key:
                self.voxelgrids = kwargs[key]
            else:
                setattr(self, key, kwargs[key])
        
        # store xyz to share memory along structures
        self.xyz = self.points[["x", "y", "z"]].values
        self.centroid = np.mean(self.xyz, axis=0)
        

    def __repr__(self):

        others = []
        for name in self.__dict__:
            if name not in ["_PyntCloud__points", "mesh", "kdtrees", "octrees", "voxelgrids", "centroid", "xyz", "neighbourhoods"]:
                others.append("\n\t " + name + ": " + str(type(name)))
        others = "".join(others)

        try:
            n_faces = len(self.mesh)
        except AttributeError:
            n_faces = 0

        return DESCRIPTION.format(  len(self.points), len(self.points.columns),
                                    n_faces,
                                    len(self.kdtrees),
                                    len(self.neighbourhoods),
                                    len(self.octrees),
                                    len(self.voxelgrids),
                                    self.centroid[0], self.centroid[1], self.centroid[2],
                                    others                                    
                                    )


    @property
    def points(self):
        return self.__points

    
    @points.setter
    def points(self, df):
        if not isinstance(df, pd.DataFrame):
            raise MUST_BE_DF

        elif not set(['x', 'y', 'z']).issubset(df.columns):
            raise MUST_HAVE_XYZ

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
            PyntCloud's instance, containing all elements in the file stored as
            PyntCloud's attributes

        """
        ext = filename.split(".")[-1].upper()

        if ext not in FORMATS_READERS.keys():
            raise UNSOPORTED_IN
        else:
            return PyntCloud( **FORMATS_READERS[ext](filename) )


    @classmethod
    def to_file(self, filename, **kwargs):
        """ Save PyntCloud's data to file 
        Parameters
        ----------
        filename : str
            Path to the file from wich the data will be readed

        """

        ext = filename.split(".")[-1].upper()

        if ext not in FORMATS_WRITERS.keys():
            raise UNSOPORTED_OUT

        else:
            if "points" not in kwargs:
                raise MUST_HAVE_POINTS

            required_args = [arg for arg in signature(FORMATS_WRITERS[ext]).parameters]

            if "kwargs" in required_args:
                FORMATS_WRITERS[ext](filename, **kwargs)
            
            else:
                valid_args = {key: kwargs[key] for key in kwargs if key in required_args} 
                FORMATS_WRITERS[ext](filename, **valid_args)

        return True

            

    def add_scalar_field(self, sf, **kwargs):
        """ Add one or multiple scalar fields to PyntCloud.points

        NEED NORMALS (nx, ny, nz):
            - 'inclination_deg'
            - 'inclination_rad'
            - 'orientation_deg'
            - 'orientation_rad'

        NEED RGB (red, green, blue):
            - 'rgb_intensity'  # adds 3 scalar fields (Ri, Gi, Bi)
            - 'hsv'  # adds 3 scalar fields (H, S, V)
            - 'relative_luminance'  
        
        NEED NEIGHBOURHOOD (from PyntCloud's neighbourhoods):
            - 'eigen_decomposition'  # adds 6 scalar fields (eigval_1, eigval_2, eigval_3, eigvec_1, eigvec_2, eigvec_3)

        NEED EIGEN_DECOMPOSITION (eigval_1, eigval_2, eigval_3, eigvec_1, eigvec_2, eigvec_3):
            - 'curvature'        
        """
        if sf in NEED_NORMALS.keys():
            normals = self.points[["nx", "ny", "nz"]].values

            if isinstance(NEED_NORMALS[sf], list):
                all_sf = getattr(scalar_fields, sf)(normals)

                for i in range(len(NEED_NORMALS[sf])):
                    self.points[NEED_NORMALS[sf][i]] = all_sf[i]

            else:
                self.points[sf] = getattr(scalar_fields, sf)(normals)


        elif sf in NEED_RGB.keys():
            rgb = self.points[["red", "green", "blue"]].values.astype("f")

            if isinstance(NEED_RGB[sf], list):
                all_sf = getattr(scalar_fields, sf)(rgb)

                for i in range(len(NEED_RGB[sf])):
                    self.points[NEED_RGB[sf][i]] = all_sf[i]

            else:
                self.points[sf] = getattr(scalar_fields, sf)(rgb)

        
        elif sf in NEED_NEIGHBOURHOOD.keys():
            neighourhood = self.xyz[self.neighbourhoods[kwargs["n_hood"]].indices]
            
            if isinstance(NEED_NEIGHBOURHOOD[sf], list):
                all_sf = getattr(scalar_fields, sf)(neighbourhood)

                for i in range(len(NEED_NEIGHBOURHOOD[sf])):
                    self.points[NEED_NEIGHBOURHOOD[sf][i]] = all_sf[i]
            
            else:
                self.points[sf] = getattr(scalar_fields, sf)(neighbourhood)
        
        else:
            raise UNSOPORTED_SF

        return str(sf) + " ADDED"

    
    def add_structure(self, structure, **kwargs):
        """ Build a structure and add it to the corresponding PyntCloud's attribute

        NEED XYZ (x, y, z):
            - 'kdtree'
            - 'voxelgrid'
        
        NEED KDTREE :
            - 'neighbourhood' # requires argument "n"  to indicate wich kdtree use

        """
        
        if structure == 'kdtree':
            valid_args = {key: kwargs[key] for key in kwargs if key in signature(KDTree).parameters}  
            kdtree = KDTree(self.xyz, **valid_args)
            self.kdtrees[kdtree.id] = kdtree

        elif structure == 'voxelgrid':            
            valid_args = {key: kwargs[key] for key in kwargs if key in signature(VoxelGrid).parameters}  
            voxelgrid = VoxelGrid(self.xyz, **valid_args)
            self.voxelgrids[voxelgrid.id] = voxelgrid
        
        elif structure == 'neighbourhood':

            valid_args = {key: kwargs[key] for key in kwargs if key in ['k', 'eps', 'p', 'distance_upper_bound']} 

            # set k=2 because first neighbour is itself 
            if 'k' not in valid_args or valid_args["k"] == 1:
                valid_args["k"] = 2
            
            neighbourhood = Neighbourhood( self.kdtrees[kwargs["kdtree"]], **valid_args)

            self.neighbourhoods[neighbourhood.id] = neighbourhood
        
        else:
            raise UNSOPORTED_STRUCTURE
        
        return str(structure) + " ADDED"
    

    def plot(self, sf=["red", "green", "blue"]):

        try:
            colors = self.points[sf].values
        except:
            colors = None
        
        if sf == ["red", "green", "blue"]:
            colors = colors/255
        else:
            colors = plt.cm.ScalarMappable().to_rgba(colors)[:,:-1]

        return plot3D(self.xyz, colors)


    def clean_SOR(self, kdtree, element='vertex', k=8, z_max=2 ):
        """ Applies a Statistical Outlier Removal filter on the given KDTree.

        Parameters
        ----------
        kdtree: scipy's KDTree instance
            The KDTree's structure which will be used to
            compute the filter.

        element(Optional): str
            The PyntCloud.element where the fillter will be apllied.

        k(Optional): int
            The number of nearest neighbors wich will be used to estimate the
            mean distance from each point to his nearest neighbors.
            Default : 8

        z_max(Optional): int
            The maximum Z score wich determines if the point is an outlier or
            not.

        Notes
        -----
        Check the filter_SOR function for more information.

        """
        cloud = getattr(self, element)

        filtered = statistical_outilier_removal(kdtree, k, z_max)

        setattr(self, element, cloud[filtered])


    def clean_ROR(self, kdtree,  k, r, element='vertex'):
        """ Applies a Radious Outlier Removal filter on the given KDTree.

        Parameters
        ----------
        kdtree: scipy's KDTree instance
            The KDTree's structure which will be used to
            compute the filter.

        k: int
            The number of nearest neighbors wich will be used to estimate the
            mean distance from each point to his nearest neighbors.

        r: float
            The radius of the sphere with center on each point and where the filter
            will look for the required number of k neighboors.

        Notes
        -----
        Check the filter_ROR function for more information.

        """

        cloud = getattr(self, element)

        filtered = radious_outlier_removal(kdtree, k, r)

        setattr(self, element, cloud[filtered])


    def clean_PT(self, element='vertex', min_x=-np.inf, max_x=np.inf,
                 min_y=-np.inf, max_y=np.inf, min_z=-np.inf, max_z=np.inf):
        """ Applies a Pass Through filter on the given element

        Parameters
        ----------
        element(Optional) : str
            The sPyntCloud's element where the function will look for the xyz
            coordinates in order to aplly the filter. Default: vertex

        Notes
        -----
        The function expects the element to have the scalar fields x,y and z
        correctly named.

        Check the filter_BB function for more information.
        """

        cloud = getattr(self, element)

        points  = cloud[['x','y','z']]

        filtered = pass_through(points, min_x, max_x, min_y, max_y, min_z, max_z)

        setattr(self, element, cloud[filtered])


    def octree_subsample(self, octree, element='vertex'):
        """ Subsamples the point cloud based on the given octree

        Parameters
        ----------
        octree : pyntcloud's VoxelGrid instance
            The Octree's structure that will be used to subsamble the point cloud

        Notes
        -----
        The function will keep only 1 point per octree's voxel, by searching in
        all the points inside an octree's voxel for the point that is nearer to
        the octree's voxel centroid.

        """

        cloud = getattr(self, element)

        cloud = pd.concat([cloud, octree.structure], axis=1)

        v2 = cloud[['x','y','z']].as_matrix()

        v1 = cloud[['centroid_x','centroid_y','centroid_z']].as_matrix()

        cloud['distances'] = np.linalg.norm(v2 - v1, axis=1)

        cloud = cloud.loc[cloud.groupby(['voxel_x','voxel_y','voxel_z'])['distances'].idxmin()]

        setattr(self, element, cloud)


    def random_subsample(self, n_points, element='vertex'):
        """ Subsamples the point cloud randomly

        Parameters
        ----------
        n_points : int
            The number of points that will have the subsampled cloud.

        """

        cloud = getattr(self, element)

        setattr(self, element, cloud.sample(n_points))
        

def vCov(data, sort=True):

    diffs = data - data.mean(1,keepdims=True)

    return np.einsum('ijk,ijl->ikl',diffs,diffs) / data.shape[1]
