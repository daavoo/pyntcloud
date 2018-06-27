=============================
Making point clouds fun again
=============================


.. image:: https://travis-ci.org/daavoo/pyntcloud.svg?branch=master
    :target: https://travis-ci.org/daavoo/pyntcloud
    :alt: Travis Build Status
    
.. image:: https://mybinder.org/badge.svg
    :target: https://mybinder.org/v2/gh/daavoo/pyntcloud/master
    :alt: Start in Binder

.. image:: /docs/images/pyntcloud_logo.png

**pyntcloud** is a Python (3, because we are not in 2008) library for working with 3D point clouds.

- Examples_ (You can try the examples without installation launching `Binder <https://mybinder.org/v2/gh/daavoo/pyntcloud/master>`_.)
- Documentation_

.. _Examples: https://github.com/daavoo/pyntcloud/tree/master/examples
.. _Documentation: http://pyntcloud.readthedocs.io/en/latest/

Overview
========

Concise API
-----------

You can access most of pyntcloud's functionality from its core class: PyntCloud.

With PyntCloud you can perform complex 3D processing operations with minimum lines of
code. For example you can:

- Load a PLY point cloud from disk.
- Add 3 new scalar fields by converting RGB to HSV.
- Build a grid of voxels from the point cloud.
- Build a new point cloud keeping only the nearest point to each occupied voxel center.
- Save the new point cloud in numpy's NPZ format.

With the following concise code:

.. code-block:: python

    from pyntcloud import PyntCloud

    cloud = PyntCloud.from_file("some_file.ply")

    cloud.add_scalar_field("hsv")

    voxelgrid_id = cloud.add_structure("voxelgrid", n_x=32, n_y=32, n_z=32)

    points = cloud.get_sample("voxelgrid_nearest", voxelgrid=voxelgrid_id)

    new_cloud = PyntCloud(points)

    new_cloud.to_file("out_file.npz")

Lightweigth visualizer
----------------------
Every PyntCloud can be visualized using the `plot` method.

The cool thing about this is that you can easily visualize point clouds inside Jupyter Notebooks and Jupyter Lab (see documentation).

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
