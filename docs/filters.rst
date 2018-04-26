.. _filters:

=======
Filters
=======

.. currentmodule:: pyntcloud

As the name suggest, filters are used to discard points from the point cloud based on a condition that is evaluated against all the points in the point cloud.

All filters take a PyntCloud (and extra information in some cases) as input and produce a boolean array as output.

This boolean array separates the points that passed the filter and will thus be retained (True) from those which did not and will thus be removed (False).

Filters are accessible through:

.. function:: PyntCloud.get_filter
    :noindex:

We group the available filters based on what the requirements for computing them are.

.. currentmodule:: pyntcloud.filters

Only require XYZ
=================

"BBOX"
------

.. autoclass:: BoundingBox

Require KDTree
==============

Required args:

    kdtree: KDTree.id

.. code-block:: python

    kdtree = pointcloud.add_structure("kdtree", ...)

"ROR"
-----

.. autoclass:: RadiusOutlierRemoval

"SOR"
-----

.. autoclass:: StatisticalOutlierRemoval
