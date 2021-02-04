.. _structures:

==========
Structures
==========

.. currentmodule:: pyntcloud

Structures are used for adding superpowers to PyntCloud instances.

For example, a `VoxelGrid` can be used for:

- Converting a point cloud into a valid input for a convolutional neural network.

- Finding nearest neighbors.

- Finding unconnected clusters of points in the point cloud.

- Many other cool things.

All structures are built on top of a point cloud, mesh or another structure.

You can create structures using:

.. function:: PyntCloud.add_structure

.. currentmodule:: pyntcloud.structures

Convex Hull
===========

.. autoclass:: ConvexHull

Delaunay3D
==========

.. autoclass:: Delaunay3D

KDTree
======

.. autoclass:: KDTree

VoxelGrid
=========

.. autoclass:: VoxelGrid
