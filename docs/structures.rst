.. _structures:

==========
Structures
==========

.. currentmodule:: pyntcloud

Structures are used for adding superpowers to PyntCloud intances.

For example, a `VoxelGrid` can be used for:

- Converting a pont cloud into a valid input for a convolutional neural networks.

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

Delanuay3D
==========

.. autoclass:: Delaunay3D

KDTree
======

.. autoclass:: KDTree

VoxelGrid
=========

.. autoclass:: VoxelGrid
