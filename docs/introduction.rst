============
Introduction
============

This page will introduce the general concept of *point clouds* and illustrate
the capabilities of pyntcloud as a point cloud processing tool.


Point clouds
============
Point clouds are one of the most relevant entities for representing three dimensional
data these days, along with polygonal meshes (which are just a special case of point clouds with
connectivity graph attached).

In its simplest form, a point cloud is a set of points in a cartesian coordinate
system.

Accurate `3D point clouds <https://en.wikipedia.org/wiki/Point_cloud>`__ can nowadays be (easily and cheaply)
acquired from different sources. For example:

- RGB-D devices: `Google Tango <http://get.google.com/tango/>`__, `Microsoft Kinect <https://developer.microsoft.com/en-us/windows/kinect>`__, etc.

- `Lidar <https://en.wikipedia.org/wiki/Lidar>`__.

- Camera + Photogrammetry software (`Open source Colmap <https://colmap.github.io/>`__, `Agisoft Photoscan <http://www.agisoft.com/>`__, . . . )

pyntcloud
=========
pyntcloud enables simple and interactive exploration of point cloud data, regardless of which sensor was used to generate it or what the use case is.

Although it was built for being used on `Jupyter Notebooks <http://jupyter.org/>`__, the library is suitable for other kinds of uses.

pyntcloud is composed of several modules (as independent as possible) that englobe
common point cloud processing operations:

-   :ref:`filters` / :ref:`filters_dev`

-   geometry

-   :ref:`io` / :ref:`io_dev`

-   learn

-   neighbors

-   plot

-   ransac

-   sampling

-   :ref:`scalar_fields` / :ref:`scalar_fields_dev`

-   :ref:`structures` / :ref:`structures_dev`

-   utils

Most of the functionality of this modules can be accessed by the core class of
the library, **PyntCloud**, and its corresponding methods:

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

Although most of the functionality in the modules can be used without constructing
a PyntCloud instance, the recommended workflow for the average user is the one showcased above.
