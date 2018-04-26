=========
PyntCloud
=========
.. currentmodule:: pyntcloud

**PyntCloud** is the core class that englobes almost all the functionality available
in **pyntcloud**.

Whereas, in its classical form, the point clouds are understood as simple sets of points, a
PyntCloud is a Python class with several **attributes** and **methods** that enable a more
fluent way of manipulating this entity.

Attributes
==========

PyntCloud's attributes serve to store information about the point cloud and the
structures associated with it.

Each PyntCloud's instance some predefined attributes:

-   centroid
-   mesh
-   :ref:`points`
-   structures
-   xyz

You may also add other attributes to your own PyntCloud instance.

The information about this attributes is reported by the __repr__ method:


.. code-block:: python

    from pyntcloud import PyntCloud

    cloud = PyntCloud.from_file("test/data/filters/filters.ply")

    print(cloud)

.. parsed-literal::

    PyntCloud
    6 points with 0 scalar fields
    0 faces in mesh
    0 kdtrees
    0 voxelgrids
    Centroid: 0.45000001788139343, 0.45000001788139343, 0.45000001788139343
    Other attributes:


Methods
=======

Available methods are very intuitive.

Methods starting with the word **add** incorporate new information to some existing PyntCloud attribute.

Methods starting with the word **get** return some information extracted from the PyntCloud.

**I/O** methods read/write information from/to different 3D formats.

**Other** methods are useful things that don't fit in any of the above categories.

*ADD* METHODS
-------------

.. function:: PyntCloud.add_scalar_field
    :noindex:

:ref:`scalar_fields`

:ref:`scalar_fields_dev`

.. function:: PyntCloud.add_structure
    :noindex:

*GET* METHODS
-------------

.. function:: PyntCloud.get_filter
    :noindex:

:ref:`filters`

:ref:`filters_dev`

.. function:: PyntCloud.get_sample
    :noindex:

:ref:`samplers`

:ref:`samplers_dev`

.. function:: PyntCloud.get_neighbors
    :noindex:

.. function:: PyntCloud.get_mesh_vertices
    :noindex:

*I/O* METHODS
-------------

:ref:`io`

.. function:: PyntCloud.from_file
    :noindex:

.. function:: PyntCloud.to_file
    :noindex:

*OTHER* METHODS
---------------

.. function:: PyntCloud.apply_filter
    :noindex:

.. function:: PyntCloud.split_on
    :noindex:

.. function:: PyntCloud.plot
    :noindex:
