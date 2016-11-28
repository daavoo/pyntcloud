#  HAKUNA MATATA


import numpy as np
import pandas as pd

from inspect import signature
from matplotlib import pyplot as plt

from .filters import F_NEIGHBOURHOOD, F_XYZ, ALL_FILTERS
from .io import FORMATS_READERS, FORMATS_WRITERS
from .plot import plot_points, DESCRIPTION
from .scalar_fields import ( 
    SF_NORMALS, SF_RGB, 
    SF_OCTREE, SF_VOXELGRID, SF_KDTREE,
    SF_OCTREE_LEVEL, SF_VOXEL_N,
    SF_EIGENVALUES,
    ALL_SF
)
from .structures import KDTree, VoxelGrid, Octree


class PyntCloud(object):
    """ A Pythonic Point Cloud
    """
    
    def __init__(self, **kwargs):  
        if "points" not in kwargs:
            raise ValueError("There must be a 'points' key in the kwargs")
        self.kdtrees = {}
        self.octrees = {}
        self.voxelgrids = {}
        self.filters = {}
        for key in kwargs:
            if "kdtrees" in key:
                self.kdtrees = kwargs[key]
            elif "octrees" in key:
                self.octrees = kwargs[key]
            elif "voxelgrids" in key:
                self.voxelgrids = kwargs[key]
            elif "filters" in key:
                self.filters = kwargs[key]
            else:
                setattr(self, key, kwargs[key])
        # store raw values to share memory along structures
        self.xyz = self.points[["x", "y", "z"]].values
        self.centroid = np.mean(self.xyz, axis=0)

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
        try:
            n_faces = len(self.mesh)
        except AttributeError:
            n_faces = 0
        return DESCRIPTION.format(  
            len(self.points), len(self.points.columns),
            n_faces,
            len(self.kdtrees),
            len(self.octrees),
            len(self.voxelgrids),
            len(self.filters),
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
        if ext not in FORMATS_READERS:
            raise ValueError("Unsupported file format; supported formats are: {}".format(list(FORMATS_READERS)))       
        else:
            return PyntCloud(**FORMATS_READERS[ext](filename))

    @classmethod
    def to_file(self, filename, **kwargs):
        """ Save PyntCloud's data to file 
        Parameters
        ----------
        filename : str
            Path to the file from wich the data will be readed
        """
        ext = filename.split(".")[-1].upper()
        if ext not in FORMATS_WRITERS:
            raise ValueError("Unsupported file format; supported formats are: {}".format(list(FORMATS_WRITERS)))
        else:
            if "points" not in kwargs:
                raise ValueError("'points' must be in kwargs")
            required_args = [x for x in signature(FORMATS_WRITERS[ext]).parameters]
            if "kwargs" in required_args:
                FORMATS_WRITERS[ext](filename, **kwargs)
            else:
                valid_args = {x: kwargs[x] for x in kwargs if x in required_args} 
                FORMATS_WRITERS[ext](filename, **valid_args)
        return True
        
    def add_scalar_field(self, sf, **kwargs):
        """ Add one or multiple scalar fields to PyntCloud.points
        """
        if sf in SF_NORMALS:
            normals = self.points[["nx", "ny", "nz"]].values
            if isinstance(SF_NORMALS[sf], tuple):
                all_sf = SF_NORMALS[sf][1](normals)
                for n, i in enumerate(SF_NORMALS[sf][0]):
                    self.points[i] = all_sf[i]
            else:
                self.points[sf] = SF_NORMALS[sf](normals)

        elif sf in SF_RGB:
            rgb = self.points[["red", "green", "blue"]].values.astype("f")
            if isinstance(SF_RGB[sf], tuple):
                all_sf = SF_RGB[sf][1](rgb)
                for n, i in enumerate(SF_RGB[sf][0]):
                    self.points[i] = all_sf[n]
            else:
                self.points[sf] = SF_RGB[sf](rgb)

        elif sf in SF_OCTREE:
            octree = self.octrees[kwargs["octree"]]
            level = kwargs["level"]
            name = "{}({},{})".format(sf, level, octree.id)
            self.points[name] = SF_OCTREE[sf](octree, kwargs["level"])

        elif sf in SF_VOXELGRID:
            voxelgrid = self.voxelgrids[kwargs["voxelgrid"]]
            name = "{}({})".format(sf, voxelgrid.id)
            self.points[name] = SF_VOXELGRID[sf](voxelgrid)

        elif sf in SF_KDTREE:
            kdtree = self.kdtrees[kwargs["kdtree"]]
            k = kwargs["k"]
            if isinstance(SF_KDTREE[sf], tuple):
                all_sf = SF_KDTREE[sf][1](kdtree, k)
                for n, i in enumerate(SF_KDTREE[sf][0]):
                    name = "{}({})".format(i, kdtree.id)
                    self.points[name] = all_sf[n]
            else:
                name = "{}({})".format(sf, kdtree.id)
                self.points[name] = SF_KDTREE[sf](kdtree, k)
        
        elif sf in SF_OCTREE_LEVEL:
            ol = kwargs["octree_level"]
            xyz_ol = self.points[["x", "y", "z", ol]]
            if isinstance(SF_OCTREE_LEVEL[sf], tuple):
                all_sf = SF_OCTREE_LEVEL[sf][1](xyz_ol, ol)
                for n, i in enumerate(SF_OCTREE_LEVEL[sf][0]):
                    name = "{}({})".format(i, ol)
                    self.points[name] = all_sf[n]
            else:
                name = "{}({})".format(sf, ol)
                self.points[name] = SF_OCTREE_LEVEL(xyz_ol, ol)

        elif sf in SF_VOXEL_N:
            vn = kwargs["voxel_n"]
            xyz_vn = self.points[["x", "y", "z", vn]]
            if isinstance(SF_VOXEL_N[sf], tuple):
                all_sf = SF_VOXEL_N[sf][1](xyz_vn, vn)
                for n, i in enumerate(SF_VOXEL_N[sf][0]):
                    name = "{}({})".format(i, vn)
                    self.points[name] = all_sf[n]
            else:
                name = "{}({})".format(sf, vn)
                self.points[name] = SF_OCTREE_LEVEL(xyz_vn, vn)

        elif sf in SF_EIGENVALUES:
            ids = ["e{}({})".format(i, kwargs["id"]) for i in range(1,4)]
            eigen_values = self.points[ids].values
            name = "{}({})".format(sf, kwargs["id"])
            self.points[name] = SF_EIGENVALUES[sf](eigen_values)

        else:
            raise ValueError("Unsupported scalar field; supported scalar fields are: {}".format(ALL_SF))

        return True

    def add_structure(self, name, **kwargs):
        """ Build a structure and add it to the corresponding PyntCloud's attribute
        """
        d = {
            'kdtree':(KDTree, self.kdtrees),
            'voxelgrid':(VoxelGrid, self.voxelgrids), 
            'octree':(Octree, self.octrees)
            }
        if name in d:
            valid_args = {x: kwargs[x] for x in kwargs if x in signature(d[name][0]).parameters}  
            structure = d[name][0](self.xyz, **valid_args)
            d[name][1][structure.id] = structure
        else:
            raise ValueError("Unsupported structure; supported structures are: {}".format(list(d)))
        return True 

    def add_filter(self, filter_name, **kwargs):
        """ Build a filter and add it to the corresponding PyntCloud's attribute
        """
        if filter_name in F_NEIGHBOURHOOD:
             n_hood = self.neighbourhoods[kwargs["n_hood"]]
             valid_args = {key: kwargs[key] for key in kwargs if key in F_NEIGHBOURHOOD[filter_name][0]} 
             filter, filter_parameter = F_NEIGHBOURHOOD[filter_name][1](n_hood, **valid_args)
             id = n_hood.id + "-{}: {}".format(filter_name, filter_parameter)
             self.filters[id] = filter  

        elif filter_name in F_XYZ:
            valid_args = {x: kwargs[x] for x in kwargs if x in F_XYZ[filter_name][0]} 
            filter, filter_parameters= F_XYZ[filter_name][1](self.xyz, **valid_args)
            self.filters["{}: {}".format(filter_name, filter_parameters)] = filter
        
        else:
            raise ValueError("Unsupported filter; supported filters are: {}".format(ALL_FILTERS))

        return True      
    
    def apply_filter(self, filter_name):
        return

    def plot(self, sf=["red", "green", "blue"], cmap="hsv", filter=None, size=0.1, axis=False, output_name=None):
        try:
            colors = self.points[sf].values
        except:
            colors = None
        if sf == ["red", "green", "blue"] and colors is not None:
            colors = colors/255
        elif colors is not None:
            s_m = plt.cm.ScalarMappable(cmap=cmap)
            colors = s_m.to_rgba(colors)[:,:-1]
        if filter is not None:
            mask = self.filters[filter]
            xyz = self.xyz[mask]
            if colors is not None:
                colors = colors[mask]
        else:
            xyz = self.xyz

        return plot_points(
            xyz=xyz,
            colors=colors, 
            size=size, 
            axis=axis, 
            output_name=output_name
            )

    
