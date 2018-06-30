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

**pyntcloud** is a Python (3, because we are not in 2008) library for working with 3D point clouds leveraging the power of the Python scientific stack.

- Examples_ (We encourage you to try the examples without installation launching `Binder <https://mybinder.org/v2/gh/daavoo/pyntcloud/master>`_.)
- Documentation_

.. _Examples: https://github.com/daavoo/pyntcloud/tree/master/examples
.. _Documentation: http://pyntcloud.readthedocs.io/en/latest/

Quick Overview
==============

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

    new_cloud = cloud.get_sample("voxelgrid_nearest", voxelgrid=voxelgrid_id, as_PyntCloud=True)

    new_cloud.to_file("out_file.npz")
