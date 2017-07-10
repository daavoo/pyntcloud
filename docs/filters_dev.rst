.. _filters_dev:

=============
Filters - Dev
=============

This page contains usefull information for developers that want to modify / add content to the filters module.

Before anithing, two big advices:

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

The sections bellow will guide you trough the filters module explaining how you can create your own filters or where you need
to look in order to modify existing ones.

Base Class
==========

.. currentmodule:: pyntcloud.filters.base

All filters must inherit from the base class `Filter` and implement it's abstract methods.

The base class is located at pyntcloud/filters/base.py

.. autoclass:: Filter     

At the very least, all filters receive a PyntCloud when they are instantiated.

The `Filter.exctract_info` method must be overrided in order to extract and save in a attribute the information required to compute the filter.

See SUBMODULE BASE CLASS bellow for more information.

`Filter.compute` is where the boolean array is generated and returned. It should use the informaction extracted by the above method in order to decide wich
points should be filtered.

See SPECIFIC FILTER CLASS bellow.

Submodule Base Class
====================

.. currentmodule:: pyntcloud.filters.f_kdtree

Filters are grouped in submodules according to wich kind of information they require to be computed.

For example, filters that require a KDTree to be computed are in pyntcloud/filters/f_kdtree.py

As the information required by all the filters in each submodule is the same, we create a submodule base class overriding the __init__ and exctract_info
methods of the Filter base class.

For example, in the f_kdtree submodule there is a Filter_KDTree class from wich all the filters that require a KDTree inherit.

.. autoclass:: Filter_KDTree     

If you don't find a submodule that extracts the information that your new filter needs, create a new one using as guideline one of the existing ones.

Specific Filter Class
=====================

Once you have a submodule base class that extracts the right information, you have to actually create the specific class 
for your filter, inheriting from the submodule base class and overriding the `Filter.compute` method.

If the computation of your filter requires some parameters from the user, you should override the `__init__` method in order to accept those
parameters.

For example, the RadiousOutlierRemoval filter requires the user to specify a radius "r" and a number of neighbors "k":

.. autoclass:: RadiousOutlierRemoval

Take a look at how this specific filter class is implemented (and documented) and use it as reference for your filters.

Let PyntCloud know about your filter
====================================

Ok, so you have come this far after all the subclassing nightmare (I can make jokes about it because I actually like it) and you have your brand new 
filter inside you brand new submodule.

Now you have to let PyntCloud know about it.

In order to do so, you have to do some things:

- Import your new filter(s) and/or submodule(s) at `pyntcloud/filters/__init__.py`.
- Include them in the ALL_FILTERS dictionary, giving them a string alias at `pyntcloud/filters/__init__.py`.
- Add tests at `test/test_filters.py`.
- (Probably) Re-write your `compute` method because tests bring bugs to light.
- Document them in the `PyntCloud.get_filter` docstring at `pyntcloud/core_class.py`.
- Document them at `docs/filters.rst`.
