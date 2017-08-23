.. _filters:

=======
Filters
=======

.. currentmodule:: pyntcloud

As the name suggest, filters are used to discard points from the point cloud based on a condition that is evaluated against all the points in the point cloud.

All filters take a PyntCloud (and extra information in some cases) as input and produce a boolean array as output.

This boolean array separates the points that passed the filter and thus will be retained (True) from those wich did not and thus will be removed (False).

Filters are accesible trough:

.. function:: PyntCloud.get_filter
    :noindex:

We group the avaliable filters based on what are the requirements for computing them.

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

.. autoclass:: RadiousOutlierRemoval

"SOR"
-----

.. autoclass:: StatisticalOutlierRemoval
