=========================
3D Point Clouds in Python
=========================

.. image:: /docs/pyntcloud_logo.png

Pyntcloud is a Python library for working with 3D point clouds.

Check the documentation at: http://pyntcloud.readthedocs.io/en/latest/index.html


QuickStart
==========

Most of the functionallity can be accesed by the core class: `PyntCloud`.

.. code-block:: python

    from pyntcloud import PyntCloud

You can load data from many 3D file formats:

.. code-block:: python

    cloud = PyntCloud.from_file("python_logo.ply")