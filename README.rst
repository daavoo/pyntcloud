=============================
Making point clouds fun again
=============================

.. image:: /docs/images/pyntcloud_logo.png

**pyntcloud** is a Python (3, because we are not in 2008) library for working with 3D point clouds.

.. image:: https://travis-ci.org/daavoo/pyntcloud.svg?branch=master
    :target: https://travis-ci.org/daavoo/pyntcloud
    :alt: Travis Build Status

- Overview_
- Documentation_

.. _Overview

Overview
========

Concise API
-----------

You can access most of pyntcloud's functionallity from it's core class: PyntCloud.

With PyntCloud you can penform complex 3D processing operations with minimum lines of 
code. For example you can:

- Load a point cloud from disk.
- Add 3 new sacalar fields by converting RGB to HSV.
- Build a grid of voxels from the point cloud.
- Build a new point cloud keeping only the points that are closest to it's corresponding voxel center.
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

Lightweigth visulizer
---------------------

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


Easy to use and extend
----------------------

Because Python. 

Check the "- Dev" sections in the documentation for extending.


.. _Documentation:

📖 Documentation
================

+---------------------------------------+--------------------------------------------------+
| `Home`_                               | Start Here.                                      |
+---------------------------------------+--------------------------------------------------+
| `Introduction`_                       | What are point clouds and what is pyntcloud.     |
+---------------------------------------+--------------------------------------------------+
| `Basic Installation`_                 | Get pyntcloud running on your computer.          |
+---------------------------------------+--------------------------------------------------+
| `Setting up a Jupyter Enviroment`_    | Get superpowers with Jupyter.                    |
+---------------------------------------+--------------------------------------------------+
| `PyntCloud`_                          | Overview of pyntcloud's core class.              |
+---------------------------------------+--------------------------------------------------+
| `Points`_                             | What is a point cloud without points?            |
+---------------------------------------+--------------------------------------------------+
| `Filters`_ // `Filters - Dev`_        | Get rid of unwanted points.                      |
+---------------------------------------+--------------------------------------------------+
| `I/O`_ // `I/O - Dev`_                | Read and write point cloud data.                 |
+---------------------------------------+--------------------------------------------------+
| `Samplers`_ // `Samplers - Dev`_      | Not related with DJ stuff. ICYI.                 |
+---------------------------------------+--------------------------------------------------+

.. _Home: http://pyntcloud.readthedocs.io/en/latest/
.. _Introduction: http://pyntcloud.readthedocs.io/en/latest/introduction.html
.. _Basic Installation: http://pyntcloud.readthedocs.io/en/latest/installation.html
.. _Setting up a Jupyter Enviroment: http://pyntcloud.readthedocs.io/en/latest/jupyter.html
.. _PyntCloud: http://pyntcloud.readthedocs.io/en/latest/PyntCloud.html
.. _Points: http://pyntcloud.readthedocs.io/en/latest/points.html
.. _Filters: http://pyntcloud.readthedocs.io/en/latest/filters.html
.. _Filters - Dev: http://pyntcloud.readthedocs.io/en/latest/filters_dev.html
.. _I/O: http://pyntcloud.readthedocs.io/en/latest/io.html
.. _I/O - Dev: http://pyntcloud.readthedocs.io/en/latest/io_dev.html
.. _Samplers: http://pyntcloud.readthedocs.io/en/latest/samplers.html
.. _Samplers - Dev: http://pyntcloud.readthedocs.io/en/latest/samplers_dev.html
