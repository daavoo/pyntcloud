#  HAKUNA MATATA


import numpy as np
import pandas as pd

from inspect import signature
from matplotlib import pyplot as plt

from .filters import *
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
{} voxelgrids
{} filters\n
Centroid: {}, {}, {}\n
Other attributes:{}        
"""

### Constant Exceptions
MUST_HAVE_POINTS = ValueError("There must be a 'points' key in the kwargs")
MUST_HAVE_XYZ = ValueError("Points must have x, y and z coordinates")
UNSOPORTED_IN = ValueError("Unsupported file format; supported formats are: "  + "  ".join(FORMATS_READERS.keys()))
UNSOPORTED_OUT = ValueError("Unsupported file format; supported formats are: "  + "  ".join(FORMATS_WRITERS.keys()))
UNSOPORTED_SF = ValueError("Unsupported scalar field; supported scalar fields are: "  + ALL_SF )
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
        self.neighbourhoods = {}
        self.octrees = {}
        self.voxelgrids = {}
        self.filters = {}

        for key in kwargs:
            if "kdtrees" in key:
                self.kdtrees = kwargs[key]
            elif "neighbourhoods" in key:
                self.neighbourhoods = kwargs[key]
            elif "octrees" in key:
                self.octrees = kwargs[key]
            elif "voxelgrids" in key:
                self.voxelgrids = kwargs[key]
            elif "filters" in key:
                self.filters = kwargs[key]
            else:
                setattr(self, key, kwargs[key])
        
        # store xyz to share memory along structures
        self.xyz = self.points[["x", "y", "z"]].values
        self.centroid = np.mean(self.xyz, axis=0)
        

    def __repr__(self):

        others = []
        for name in self.__dict__:
            if name not in ["_PyntCloud__points", "mesh", "kdtrees", "octrees", "voxelgrids", "centroid", "xyz", "neighbourhoods", "filters"]:
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
                                    len(self.filters),
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

        NEED NORMALS 
            - 'inclination_deg'
            - 'inclination_rad'
            - 'orientation_deg'
            - 'orientation_rad'

        NEED RGB 
            - 'rgb_intensity': [Ri, Gi, Bi]
            - 'hsv': [H, S, V]
            - 'relative_luminance'  
        
        NEED NEIGHBOURHOOD
            - 'eigen_values': [{}-e1, {}-e2, {}-e3]   # {}: neighbourhood.id
            - 'eigen_sum'
            - 'omnivariance'
            - 'eigenentropy'
            - 'anisotropy'
            - 'planarity'
            - 'linearity'
            - 'curvature'
            - 'sphericity'
            - 'verticality'       
        """
        if sf in SF_NORMALS.keys():
            normals = self.points[["nx", "ny", "nz"]].values

            if isinstance(SF_NORMALS[sf], tuple):
                all_sf = SF_NORMALS[sf][1](normals)

                for i, name in enumerate(SF_NORMALS[sf][0]):
                    self.points[name] = all_sf[i]

            else:
                self.points[sf] = SF_NORMALS[sf](normals)


        elif sf in SF_RGB.keys():
            rgb = self.points[["red", "green", "blue"]].values.astype("f")

            if isinstance(SF_RGB[sf], tuple):
                all_sf = SF_RGB[sf][1](normals)

                for i, name in enumerate(SF_RGB[sf][0]):
                    self.points[name] = all_sf[i]

            else:
                self.points[sf] = SF_RGB[sf](rgb)

        
        elif sf in SF_NEIGHBOURHOOD.keys():
            n_hood = self.neighbourhoods[kwargs["n_hood"]]
            
            if isinstance(SF_NEIGHBOURHOOD[sf], tuple):
                all_sf = SF_NEIGHBOURHOOD[sf][1](n_hood)

                for i, name in enumerate(SF_NEIGHBOURHOOD[sf][0]):
                    id = n_hood.id + "-{}".format(name)
                    self.points[id] = all_sf[i]
            
            else:
                id = n_hood.id + "-{}".format(sf)
                self.points[id] = SF_NEIGHBOURHOOD[sf](n_hood)
        
        else:
            raise UNSOPORTED_SF

        return "Added: " + str(sf)

    
    def add_structure(self, structure_name, **kwargs):
        """ Build a structure and add it to the corresponding PyntCloud's attribute

        NEED XYZ:
            - 'kdtree'
            - 'voxelgrid'
        
        NEED KDTREE:
            - 'neighbourhood'

        """
        
        if structure_name == 'kdtree':
            valid_args = {key: kwargs[key] for key in kwargs if key in signature(KDTree).parameters}  
            structure = KDTree(self.xyz, **valid_args)
            self.kdtrees[structure.id] = structure

        elif structure_name == 'voxelgrid':            
            valid_args = {key: kwargs[key] for key in kwargs if key in signature(VoxelGrid).parameters}  
            structure = VoxelGrid(self.xyz, **valid_args)
            self.voxelgrids[structure.id] = structure
        
        elif structure_name == 'neighbourhood':

            valid_args = {key: kwargs[key] for key in kwargs if key in ['k', 'eps', 'p', 'distance_upper_bound']} 

            if 'k' not in valid_args:
                valid_args["k"] = 2
            else:
                # +1 because first neighbour is itself 
                valid_args["k"] += 1
            
            structure = Neighbourhood( self.kdtrees[kwargs["kdtree"]], **valid_args)

            self.neighbourhoods[structure.id] = structure
        
        else:
            raise UNSOPORTED_STRUCTURE
        
        return "Added: " + str(structure_name) + " " +  structure.id 


    def add_filter(self, filter_name, **kwargs):
        """ Build a filter and add it to the corresponding PyntCloud's attribute
        
        NEED NEIGHBOURHOOD:
            - 'SOR'
            - 'ROR'
        """

        if filter_name in F_NEIGHBOURHOOD.keys():
             n_hood = self.neighbourhoods[kwargs["n_hood"]]

             valid_args = {key: kwargs[key] for key in kwargs if key in F_NEIGHBOURHOOD[filter_name][0]} 

             filter, filter_parameter = F_NEIGHBOURHOOD[filter_name][1](n_hood, **valid_args)

             id = n_hood.id + "-{}-{}".format(filter_name, filter_parameter)
             
             self.filters[id] = filter  

        return "Added: " + str(filter_name)       
    

    def plot(self, sf=["red", "green", "blue"], cmap="hsv", filter=None, size=0.1, axis=True ):

        try:
            colors = self.points[sf].values
        except:
            colors = None
        
        if sf == ["red", "green", "blue"]:
            colors = colors/255
        else:
            s_m = plt.cm.ScalarMappable(cmap=cmap)
            colors = s_m.to_rgba(colors)[:,:-1]
        
        if filter is not None:
            mask = self.filters[filter]
            xyz = self.xyz[mask]
            if colors is not None:
                colors = colors[mask]
        else:
            xyz = self.xyz

        return plot3D(xyz=xyz, colors=colors, size=size, axis=axis)


    def random_subsample(self, n_points, element='vertex'):
        """ Subsamples the point cloud randomly

        Parameters
        ----------
        n_points : int
            The number of points that will have the subsampled cloud.

        """

        cloud = getattr(self, element)

        setattr(self, element, cloud.sample(n_points))
