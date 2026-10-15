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

Scalar Fields are accessible trough:

.. function:: PyntCloud.add_scalar_field
    :noindex:

We group the available scalar fields based on what the requirements for computing them are.

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

"eigen_sum"
------------

.. autoclass:: EigenSum

"linearity"
------------

.. autoclass:: Linearity


"omnivariance"
--------------

.. autoclass:: Omnivariance

"planarity"
-----------

.. autoclass:: Planarity

"sphericity"
------------

.. autoclass:: Sphericity

Require K Neighbors
===================

Required args:

    k_neighbors: (N, k) ndarray

.. code-block:: python

    k_neighbors = pointcloud.get_neighbors(k=10)

"normals"
---------

.. autoclass:: UnorientedNormals

"eigen_values"
--------------

.. autoclass:: EigenValues

"eigen_decomposition"
---------------------

.. autoclass:: EigenDecomposition

Require Normals
===============

`pointcloud.points` must have [nx, ny, nz] columns.

"inclination_degrees"
---------------------

.. autoclass:: InclinationDegrees

"inclination_radians"
---------------------

.. autoclass:: InclinationRadians

"orientation_degrees"
---------------------

.. autoclass:: OrientationDegrees

"orientation_radians"
---------------------

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

    voxelgrid_id: VoxelGrid.id

.. code-block:: python

    voxelgrid_id = pointcloud.add_structure("voxelgrid")

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
