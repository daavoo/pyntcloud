=============================
Making point clouds fun again
=============================


.. image:: https://travis-ci.org/daavoo/pyntcloud.svg?branch=master
    :target: https://travis-ci.org/daavoo/pyntcloud
    :alt: Travis Build Status

.. image:: /docs/images/pyntcloud_logo.png

**pyntcloud** is a Python (3, because we are not in 2008) library for working with 3D point clouds.

- Documentation_
- Overview_

.. _Documentation:

Documentation 
=============
📖 📖


+---------------------------------------+
| `Home`_                               |
+---------------------------------------+
| `Introduction`_                       |
+---------------------------------------+
| `Installation`_                       |
+---------------------------------------+
| `PyntCloud`_                          |
+---------------------------------------+
| `Points`_                             |
+---------------------------------------+
| `Filters`_ // `Filters - Dev`_        |
+---------------------------------------+
| `I/O`_ // `I/O - Dev`_                |
+---------------------------------------+
| `Samplers`_ // `Samplers - Dev`_      |
+---------------------------------------+
| `Structures`_ // `Structures - Dev`_  |
+---------------------------------------+


.. _Home: http://pyntcloud.readthedocs.io/en/latest/
.. _Introduction: http://pyntcloud.readthedocs.io/en/latest/introduction.html
.. _Installation: http://pyntcloud.readthedocs.io/en/latest/installation.html
.. _PyntCloud: http://pyntcloud.readthedocs.io/en/latest/PyntCloud.html
.. _Points: http://pyntcloud.readthedocs.io/en/latest/points.html
.. _Filters: http://pyntcloud.readthedocs.io/en/latest/filters.html
.. _Filters - Dev: http://pyntcloud.readthedocs.io/en/latest/filters_dev.html
.. _I/O: http://pyntcloud.readthedocs.io/en/latest/io.html
.. _I/O - Dev: http://pyntcloud.readthedocs.io/en/latest/io_dev.html
.. _Samplers: http://pyntcloud.readthedocs.io/en/latest/samplers.html
.. _Samplers - Dev: http://pyntcloud.readthedocs.io/en/latest/samplers_dev.html
.. _Structures: http://pyntcloud.readthedocs.io/en/latest/structures.html
.. _Structures - Dev: http://pyntcloud.readthedocs.io/en/latest/structures_dev.html

.. _Overview:

Overview
========

Concise API
-----------

You can access most of pyntcloud's functionality from its core class: PyntCloud.

With PyntCloud you can perform complex 3D processing operations with minimum lines of
code. For example you can:

- Load a point cloud from disk.
- Add 3 new scalar fields by converting RGB to HSV.
- Build a grid of voxels from the point cloud.
- Build a new point cloud keeping only the nearest point to each occupied voxel center.
- Save the new point cloud.

With the following concise code:

.. code-block:: python

    from pyntcloud import PyntCloud

    cloud = PyntCloud.from_file("some_file.ply")

    cloud.add_scalar_field("hsv")

    voxelgrid_id = cloud.add_structure("voxelgrid", x_y_z=[32, 32, 32])

    points = cloud.get_sample("voxelgrid_nearest", voxelgrid=voxelgrid_id)

    new_cloud = PyntCloud(points)

    new_cloud.to_file("out_file.ply")

Lightweigth visualizer
----------------------

Every PyntCloud can be visualized using the `plot` method.

This will create a stand-alone html visualizer. The cool thing about this is that
you can open it in any browser and if you call it from inside a Jupyter Notebook, the
visualizer will be embedded as an IFrame:

.. image:: /docs/images/plot1.gif

The plot function has many options.

For example you can use any scalar field as color with a custom colormap:

.. image:: /docs/images/plot2.gif

Or, if it exists, visualize the mesh associated with the point cloud:

.. image:: /docs/images/plot3.gif


General purpose
----------------

Even though point clouds obtained from different sources present some variance in terms of the kind of information they contain,
we encourage a source-agnostic vision of point clouds.

pyntcloud provides tools for source-agnostic 3D processing operations but it also provides building blocks for easily implementing something
that covers your specific needs.

Easy to use and extend
----------------------

Because Python.
