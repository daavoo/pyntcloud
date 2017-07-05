.. _filters:

=============
About Filters
=============

.. currentmodule:: pyntcloud

As the name suggest, filters are used to discard points from the point cloud based on a condition that is evaluated against all the points in the point cloud.

All filters take a point cloud as input and produce a boolean array as output.

This boolean array separates the points that passed the filter and thus will be retained (True) from those wich did not and thus will be removed (False).

Filters are accesible trough PyntCloud's method: get_filter() passing the corresponding string alias as first argument.


We group the avaliable filters based on what are the requirements for computing them.

Only require XYZ
=================

"BBOX" (Bounding Box)
---------------------

.. automethod:: filters.BoundingBox

Require KDTree
=================

"ROR" (Radius Outlier Removal)
------------------------------

.. automethod:: filters.RadiousOutlierRemoval

"SOR" (Statistical Outlier Removal)
-----------------------------------

.. automethod:: filters.StatisticalOutlierRemoval
