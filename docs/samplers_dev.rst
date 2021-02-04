.. _samplers_dev:

==============
Samplers - Dev
==============

This page contains useful information for developers who want to modify / add content to the samplers module.

First of all, two points of advice:

- Use the existing samplers as guideline.

- Follow the general CONTRIBUTING GUIDELINES.

The Big Picture
===============

.. currentmodule:: pyntcloud

Filters are used by the method:

.. function:: PyntCloud.get_sampler
    :noindex:

Take a look at the source code in order to get a general overview of how samplers are being used. All samplers are classes and all have the same
methods.

The sections below will guide you trough the samplers module explaining how you can create your own samplers or where you need
to look in order to modify existing ones.

Base Class
==========

.. currentmodule:: pyntcloud.samplers.base

All samplers must inherit from the base class `Sampler` and implement its abstract methods.

The base class is located at pyntcloud/filters/base.py

.. autoclass:: Sampler

At the very least, all samplers receive a PyntCloud when they are instantiated.

The `Sampler.extract_info` method must be overridden in order to extract and save the information required to generate the sample in a attribute.

See SUBMODULE BASE CLASS below for more information.

`Sampler.compute` is where the sample is generated and returned. It should use the information extracted by the above method in order to generate the sample.

See SPECIFIC SAMPLER CLASS below.

Submodule Base Class
====================

.. currentmodule:: pyntcloud.samplers.s_voxelgrid

Samplers are grouped into submodules according to which kind of information they require to be computed.

For example, samplers that require a VoxelGrid to be computed are in pyntcloud/samplers/s_voxelgrid.py

As the information required by all the filters in each submodule is the same, we create a submodule base class overriding the __init__ and extract_info
methods of the Sampler base class.

For example, in the s_voxelgrid submodule there is a Sampler_Voxelgrid class from which all the samplers that require a Voxelgrid inherit.

.. autoclass:: Sampler_Voxelgrid

If you don't find a submodule that extracts the information that your new sampler needs, create a new one using as guideline one of the existing ones.

Specific Sampler Class
======================

.. currentmodule:: pyntcloud.samplers.s_mesh

Once you have a submodule base class that extracts the right information, you have to actually create the specific class
for your sampler, inheriting from the submodule base class and overriding the `Sampler.compute` method.

If the computation of your sample requires some parameters from the user, you should override the `__init__` method in order to accept those
parameters.

For example, the `RandomMesh` sampler requires the user to specify if the sample will use RGB and/or normal information:

.. autoclass:: RandomMesh

Let PyntCloud know about your sampler
=====================================

In order to do so, you have to do some things:

- Add tests at `test/test_samplers.py`.
- Import your new sampler(s) and/or submodule(s) at `pyntcloud/samplers/__init__.py`.
- Include them in the ALL_SAMPLERS dictionary, giving them a **string alias**, at `pyntcloud/samplers/__init__.py`.
- Document them in the `PyntCloud.get_sample` docstring at `pyntcloud/core_class.py`.
- Document them at `docs/samplers.rst`.
