=========
PyntCloud
=========
.. currentmodule:: pyntcloud

**PyntCloud** is the core class that englobes almost all the functionallity avaliable
in **pyntcloud**.

Whereas, in it's classical form, the point clouds are understood as simple sets of points, a
PyntCloud is a Python class with several **attributes** and **methods** that enable a more
fluent way of manipulating this entities.

Attributes
==========

PyntCloud's attributes serve to store information about the point cloud and the
structures associated with it.

Each PyntCloud's instance some predifined attributes:

-   centroid
-   mesh
-   points - :ref:`working-with-points`
-   structures
-   xyz

You may also add other attributes to your own PyntCloud's instance.

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

Avaliable methods are very intuitive.

Methods starting with the word **add** will incorporate new information to some existing PyntCloud attribute.

Methods starting with the word **get** will return some information extracted from the PyntCloud.

I/O methods are documented in :ref:`reading-and-writing`.

*ADD* METHODS
-------------

.. automethod:: PyntCloud.add_scalar_field

.. automethod:: PyntCloud.add_structure

*GET* METHODS
-------------

.. automethod:: PyntCloud.get_filter

.. automethod:: PyntCloud.get_sample

.. automethod:: PyntCloud.get_neighbors
