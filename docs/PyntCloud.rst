=========
PyntCloud
=========

**PyntCloud** is the core class that englobes almost all the functionallity avaliable
in **pyntcloud**.

This class was designed as a programming-focused extension of the original concept of point cloud.

Whereas in it's classical form the point clouds are understood as simple sets of points, a 
PyntCloud is a Python class with several **attributes** and **methods** that enable a more
fluent way of manipulating this entities.

Attributes
==========

PyntCloud's attributes serve to store information that might be used by PyntCloud's
methods.

Each PyntCloud's instance contains the following attributes:

-   centroid
-   kdtrees
-   mesh
-   octrees
-   points

This is the only attribute that can't be empty.

-   voxelgrids
-   xyz

You may also add other attributes to your own PyntCloud's instance.

The information about this attributes is reported by the __repr__ method:


.. code-block:: python

    from pyntcloud import PyntCloud
    
    cloud = PyntCloud.from_file("test/data/filters/filters.ply")   
    
    print(cloud)
    """
    PyntCloud
    6 points with 0 scalar fields
    0 faces in mesh
    0 kdtrees
    0 octrees
    0 voxelgrids
    Centroid: 0.45000001788139343, 0.45000001788139343, 0.45000001788139343
    Other attributes: 
    """
