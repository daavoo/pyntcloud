.. _filters_dev:

=============
Filters - Dev
=============

This page contains useful information for developers who want to modify / add content to the filters module.

First of all, two points of advice:

- Use the existing filters as guideline.

- Follow the general CONTRIBUTING GUIDELINES.

The Big Picture
===============

.. currentmodule:: pyntcloud

Filters are used by the method:

.. function:: PyntCloud.get_filter
    :noindex:

Take a look at the source code in order to get a general overview of how filters are being used. All filters are classes and all have the same
methods.

The sections below will guide you through the filters module explaining how you can create your own filters or where you need
to look in order to modify existing ones.

Base Class
==========

.. currentmodule:: pyntcloud.filters.base

All filters must inherit from the base class `Filter` and implement its abstract methods.

The base class is located at pyntcloud/filters/base.py

.. autoclass:: Filter

At the very least, all filters receive a PyntCloud when they are instantiated.

The `Filter.extract_info` method must be overridden in order to extract and save the information required to compute the filter in a attribute.

See SUBMODULE BASE CLASS below for more information.

`Filter.compute` is where the boolean array is generated and returned. It should use the information extracted by the above method in order to decide which
points should be filtered.

See SPECIFIC FILTER CLASS below.

Submodule Base Class
====================

.. currentmodule:: pyntcloud.filters.f_kdtree

Filters are grouped into submodules according to which kind of information they require to be computed.

For example, filters that require a KDTree to be computed are in pyntcloud/filters/f_kdtree.py

As the information required by all the filters in each submodule is the same, we create a submodule base class overriding the __init__ and extract_info
methods of the Filter base class.

For example, in the f_kdtree submodule there is a Filter_KDTree class from which all the filters that require a KDTree inherit.

.. autoclass:: Filter_KDTree

If you don't find a submodule that extracts the information that your new filter needs, create a new one using as guideline one of the existing ones.

Specific Filter Class
=====================

Once you have a submodule base class that extracts the right information, you have to actually create the specific class
for your filter, inheriting from the submodule base class and overriding the `Filter.compute` method.

If the computation of your filter requires some parameters from the user, you should override the `__init__` method in order to accept those
parameters.

For example, the RadiusOutlierRemoval filter requires the user to specify a radius "r" and a number of neighbors "k":

.. autoclass:: RadiusOutlierRemoval

Let PyntCloud know about your filter
====================================

In order to do so, you have to do some things:

- Add tests at `test/test_filters.py`.
- Import your new filter(s) and/or submodule(s) at `pyntcloud/filters/__init__.py`.
- Include them in the ALL_FILTERS dictionary, giving them a **string alias** at `pyntcloud/filters/__init__.py`.
- Document them in the `PyntCloud.get_filter` docstring at `pyntcloud/core_class.py`.
- Document them at `docs/filters.rst`.
