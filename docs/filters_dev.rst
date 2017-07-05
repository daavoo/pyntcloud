.. _filters_dev:

======================
[DEVELOPERS] - Filters
======================

.. currentmodule:: pyntcloud.filters.base

This page contains usefull information for developers that want to modify / add content to the filter module.

BASE CLASS
==========

All filters must inherit from the base class `Filter` and implement it's abstract methods.

The base class is located at pyntcloud/filters/base.py

.. autoclass:: Filter     
   :members: 

   .. automethod:: __init__

   .. automethod:: extract_info

   .. automethod:: compute