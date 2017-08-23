.. _scalar_fields:

=============
Scalar Fields
=============

.. currentmodule:: pyntcloud

Roughly speaking, each of the columns in the `PyntCloud.points` DataFrame is a Scalar Field.

Point clouds require at least 3 columns to be defined (the x,y,z coordinates); any other information associated to each point is a Scalar Field.

For example point clouds with color information usually have 3 scalar fields representing the Red, Green, and Blue values for each point.

A Scalar Field must have the same type and meaning for every point, the value is what is variable.

In the point cloud literature, Scalar Fields are restricted to be numeric (that’s where the Scalar comes from), but here we extend the Scalar Field term to defined any column of the Points DataFrame.

Scalar Fields are accesible trough:

Scalar Fields are accesible trough:

.. function:: PyntCloud.get_filter
    :noindex:

We group the avaliable scalar fields based on what are the requirements for computing them.

.. currentmodule:: pyntcloud.scalar_fields

Only require XYZ
=================

"plane_fit"
-----------

.. autoclass:: PlaneFit


"sphere_fit"
------------

.. autoclass:: SphereFit


"custom_fit"
------------

.. autoclass:: CustomFit

"spherical_coords"
------------------

.. autoclass:: SphericalCoordinates

Require Eigen Values
====================

Required args:

    ev: list of str

.. code-block:: python

    ev = pointcloud.add_scalar_field("eigen_values", ...)


"anisotropy"
------------

.. autoclass:: Anisotropy

"curvature"
------------

.. autoclass:: Curvature

"eigenentropy"
--------------

.. autoclass:: Eigenentropy

"eigensum"
------------

.. autoclass:: EigenSum

"linearity"
------------

.. autoclass:: Linearity


"ommnivariance"
---------------

.. autoclass:: Omnivariance

"planarity"
-----------

.. autoclass:: Planarity

"sphericity"
------------

.. autoclass:: Planarity

Require K Neighbors
===================

Required args:

    k_neighbors: (N, k) ndarray

.. code-block:: python

    k_neighbros = pointcloud.get_k_neighbors(k=10, ...)

"normals"
---------

.. autoclass:: Normals

"eigen_values"
--------------

.. autoclass:: EigenValues

"eigen_decomposition"
---------------------

.. autoclass:: EigenDecomposition

Require Normals
===============

`pointcloud.points` must have [nx, ny, nz] columns.

"inclination_deg"
-----------------

.. autoclass:: InclinationDegrees

"inclination_rad"
-----------------

.. autoclass:: InclinationRadians

"orientation_deg"
-----------------

.. autoclass:: OrientationDegrees

"orientation_rad"
-----------------

.. autoclass:: OrientationRadians

Require RGB
===========

`pointcloud.points` must have [red, green, blue] columns.

"hsv"
-----

.. autoclass:: HueSaturationValue

"relative_luminance"
--------------------

.. autoclass:: RelativeLuminance

"rgb_intensity"
---------------

.. autoclass:: RGBIntensity

Require VoxelGrid
=================

Required args:

    voxelgrid: VoxelGrid.id

.. code-block:: python

    voxelgrid = self.add_structure("voxelgrid", ...)

"euclidean_clusters"
--------------------

.. autoclass:: EuclideanClusters

"voxel_n"
---------

.. autoclass:: VoxelN

"voxel_x"
---------

.. autoclass:: VoxelX

"voxel_y"
---------

.. autoclass:: VoxelY

"voxel_z"
---------

.. autoclass:: VoxelZ
