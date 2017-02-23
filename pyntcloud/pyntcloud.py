#  HAKUNA MATATA


import numpy as np
import pandas as pd

from matplotlib import pyplot as plt

from .filters import (
    F_KDTREE,
    F_XYZ,
    ALL_FILTERS
)
from .io import FROM, TO
from .plot import plot_points, DESCRIPTION
from .scalar_fields import ( 
    SF_RANSAC,
    SF_NORMALS, SF_RGB, 
    SF_OCTREE, SF_VOXELGRID, SF_KDTREE,
    SF_EIGENVALUES,
    ALL_SF
)
from .structures import KDTree, VoxelGrid, Octree
from .utils.misc import crosscheck_kwargs_function


class PyntCloud(object):
    """ A Pythonic Point Cloud
    """
    
    def __init__(self, **kwargs):  
        if "points" not in kwargs:
            raise ValueError("There must be a 'points' key in the kwargs")
        self.points = kwargs["points"]
        del kwargs["points"]
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
        """
        
        ext = filename.split(".")[-1].upper()
        if ext not in TO:
            raise ValueError("Unsupported file format; supported formats are: {}".format(list(TO)))
        kwargs["filename"] = filename
        for x in internal:
            kwargs[x] = getattr(self, x)
        valid_args =  crosscheck_kwargs_function(kwargs, TO[ext])
        TO[ext](**valid_args)

        return True
        
    def add_scalar_field(self, sf, **kwargs):
        """ Add one or multiple scalar fields to PyntCloud.points
        """
                
        if sf in SF_RANSAC:
            kwargs["points"] = self.xyz
            valid_kwargs = crosscheck_kwargs_function(kwargs, SF_RANSAC[sf][1])
            all_sf = SF_RANSAC[sf][1](**valid_kwargs)
            for n, i in enumerate(SF_RANSAC[sf][0]):
                self.points[i] = all_sf[n]
                print("{} added".format(i))
        
        elif sf in SF_NORMALS:
            kwargs["normals"] = self.points[["nx", "ny", "nz"]].values
            valid_kwargs = crosscheck_kwargs_function(kwargs, SF_NORMALS[sf][1])
            all_sf = SF_NORMALS[sf][1](**valid_kwargs)
            for n, i in enumerate(SF_NORMALS[sf][0]):
                self.points[i] = all_sf[n]
                print("{} added".format(i))

        elif sf in SF_RGB:
            kwargs["rgb"] = self.points[["red", "green", "blue"]].values.astype("f")
            valid_kwargs = crosscheck_kwargs_function(kwargs, SF_RGB[sf][1])
            all_sf = SF_RGB[sf][1](**valid_kwargs)
            for n, i in enumerate(SF_RGB[sf][0]):
                self.points[i] = all_sf[n]
                print("{} added".format(i))

        elif sf in SF_OCTREE:
            kwargs["octree"] = self.octrees[kwargs["octree"]]
            valid_kwargs = crosscheck_kwargs_function(kwargs, SF_OCTREE[sf][1])
            all_sf = SF_OCTREE[sf][1](**valid_kwargs)
            for n, i in enumerate(SF_OCTREE[sf][0]):
                name = "{}({},{})".format(i, valid_kwargs["level"], valid_kwargs["octree"].id)
                self.points[name] = all_sf[n]
                print("{} added".format(name))

        elif sf in SF_VOXELGRID:
            kwargs["voxelgrid"] = self.voxelgrids[kwargs["voxelgrid"]]
            valid_kwargs = crosscheck_kwargs_function(kwargs, SF_VOXELGRID[sf][1])
            all_sf = SF_VOXELGRID[sf][1](**valid_kwargs)
            for n, i in enumerate(SF_VOXELGRID[sf][0]):
                name = "{}({})".format(i, valid_kwargs["voxelgrid"].id)
                self.points[name] = all_sf[n]
                print("{} added".format(name))

        elif sf in SF_KDTREE:
            kwargs["kdtree"] = self.kdtrees[kwargs["kdtree"]]
            valid_kwargs = crosscheck_kwargs_function(kwargs, SF_KDTREE[sf][1])
            all_sf = SF_KDTREE[sf][1](**valid_kwargs)
            for n, i in enumerate(SF_KDTREE[sf][0]):
                name = "{}({})".format(i, valid_kwargs["kdtree"].id)
                self.points[name] = all_sf[n]
                print("{} added".format(name))

        elif sf in SF_EIGENVALUES:
            ids = ["e{}({})".format(i, kwargs["id"]) for i in range(1,4)]
            kwargs["eigen_values"] = self.points[ids].values
            valid_kwargs = crosscheck_kwargs_function(kwargs, SF_EIGENVALUES[sf][1])
            all_sf = SF_EIGENVALUES[sf][1](**valid_kwargs)
            for n, i in enumerate(SF_KDTREE[sf][0]):
                name = "{}({})".format(i, kwargs["id"])
                self.points[name] = all_sf[n]
                print("{} added".format(name))

        else:
            raise ValueError("Unsupported scalar field; supported scalar fields are: {}".format(ALL_SF))

        return True

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
        print("{} added".format(structure.id))
        return True 

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
            
    def _clean_all_structures(self):
        self.kdtrees = {}
        self.voxelgrids = {}
        self.octrees = {}


    
