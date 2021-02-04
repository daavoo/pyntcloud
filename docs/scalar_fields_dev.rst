.. _scalar_fields_dev:

===================
Scalar Fields - Dev
===================


This page contains useful information for developers that want to modify / add content to the scalar_fields module.

First of all, two points of advice:

- Use the existing scalar_fields as guideline.

- Follow the general CONTRIBUTING GUIDELINES.

The Big Picture
===============

.. currentmodule:: pyntcloud

Filters are used by the method:

.. function:: PyntCloud.add_scalar_field
    :noindex:

Take a look at the source code in order to get a general overview of how scalar fields are being used. All scalar fields are classes and all have the same
methods.

The sections below will guide you trough the scalar fields module explaining how you can create your own scalar fields or where you need
to look in order to modify existing ones.

Base Class
==========

.. currentmodule:: pyntcloud.scalar_fields.base

All filters must inherit from the base class `ScalarField` and implement its abstract methods.

The base class is located at pyntcloud/scalar_fields/base.py

.. autoclass:: ScalarField

At the very least, all scalar fields receive a PyntCloud when they are instantiated.

The `ScalarField.extract_info` method must be overridden in order to extract and save in a attribute the information required to compute the scalar field.

See SUBMODULE BASE CLASS below for more information.

`ScalarField.compute` is where the new DataFrame columns are generated.

See SPECIFIC SCALAR FIELD CLASS below.

Submodule Base Class
====================

.. currentmodule:: pyntcloud.scalar_fields.sf_voxelgrid

Scalar fields are grouped in submodules according to which kind of information they require to be computed.

For example, scalar fields that require a VoxelGrid to be computed are in pyntcloud/scalar_fields/sf_voxelgrid.py

As the information required by all the scalar fields in each submodule is the same, we create a submodule base class overriding the __init__ and extract_info
methods of the ScalarField base class.

For example, in the sf_voxelgrid submodule there is a ScalarField_Voxelgrid class from which all the scalar fields that require a VoxelGrid inherit.

.. autoclass:: ScalarField_Voxelgrid

If you don't find a submodule that extracts the information that your new scalar field needs, create a new one using as guideline one of the existing ones.

Specific Scalar Field Class
===========================

Once you have a submodule base class that extracts the right information, you have to actually create the specific class
for your scalar field, inheriting from the submodule base class and overriding the `ScalarField.compute` method.

If the computation of your scalar requires some parameters from the user, you should override the `__init__` method in order to accept those
parameters.

.. currentmodule:: pyntcloud.scalar_fields.sf_xyz

For example, the SphericalCoordinates scalar field (in pyntcloud/scalar_fields/sf_xyz.py) requires the user to specify if the output should be in degrees or not:

.. autoclass:: SphericalCoordinates

Let PyntCloud know about your filter
====================================

In order to do so, you have to do some things:

- Add tests at `test/test_sf.py`.
- Import your new scalar field(s) and/or submodule(s) at `pyntcloud/scalar_fields/__init__.py`.
- Include them in the ALL_SF dictionary, giving them a **string alias** at `pyntcloud/scalar_fields/__init__.py`.
- Document them in the `PyntCloud.add_scalar_field` docstring at `pyntcloud/core_class.py`.
- Document them at `docs/scalar_fields.rst`.
