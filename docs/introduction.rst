============
Introduction
============

This page will introduce the general concept of *point clouds* and illustrate
what are the capabilities of pyntcloud as a point cloud processing tool.


Point clouds
============
Point clouds are one of the most relevant entities for representing three dimensional
data these days, along with polygonal meshes (wich are just a special case of point clouds with
connectivity graph attached).

In it's simplest form, a point cloud is a set of points in a cartesian coordinate
system.

Accurate `3D point clouds <https://en.wikipedia.org/wiki/Point_cloud>`__ can (easily and cheaply)
be adquired nowdays from different sources. For example:

- RGB-D devices: `Google Tango <http://get.google.com/tango/>`__, `Microsoft Kinect <https://developer.microsoft.com/en-us/windows/kinect>`__, etc.

- `Lidar <https://en.wikipedia.org/wiki/Lidar>`__.

- Camera + Photogrammetry software (`Open source Colmap <https://colmap.github.io/>`__, `Agisoft Photoscan <http://www.agisoft.com/>`__, . . . )

pyntcloud
=========
pyntcloud enables simple and interactive exploration of point cloud data, regardless of which sensor was used to generate it or what is the use case.

Althoug it was built for being used on `Jupyter Notebooks <http://jupyter.org/>`__ the library is suitable for other kind of uses.

pyntcloud is composed by several modules (as indepentent as possible) that englobe
commom point cloud processing operations:

-   filters
-   geometry
-   io
-   learn
-   neighbors
-   plot
-   ransac
-   sampling
-   scalar_fields
-   structures
-   utils

Most of the functionallity of this modules can be accesed by the core class of
the library, **PyntCloud**, and it's corresponding methods:

.. code-block:: python

    from pyntcloud import PyntCloud
    # io
    cloud = PyntCloud.from_file("some_file.ply")
    # structures
    kdtree_id = cloud.add_structure("kdtree")
    # neighbors
    k_neighbors = cloud.get_neighbors(k=5, kdtree=kdtree_id)
    # scalar_fields
    ev = cloud.add_scalar_field("eigen_values", k_neighbors=k_neighbors)
    # filters
    f = cloud.get_filter("BBOX", min_x=0.1, max_x=0.8)
    # ...

Although most of the functionallity in the modules can be used without constructing
a PyntCloud instance, the recommended workflow for the average user is the one showcased above.
