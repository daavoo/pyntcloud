.. _reading-and-writing:

===================
Reading and writing
===================
.. currentmodule:: pyntcloud

As mentioned in the introduction, 3D point clouds could be obtained from many 
different sources, each one with it's own file format.

In addition to file formats used by each manufacturer, point cloud may also be
stored in generic binary and ascii formats using different programming languages. 

pyntcloud provides reading and writing routines from many common 3D file and
generic array formats (more formats will be added in the near future):

-   `.mat <https://es.mathworks.com/help/matlab/import_export/mat-file-versions.html>`__
-   `.npy / .npz <https://docs.scipy.org/doc/numpy-dev/neps/npy-format.html>`__
-   `.obj <https://en.wikipedia.org/wiki/Wavefront_.obj_file>`__
-   `.off <https://en.wikipedia.org/wiki/OFF_(file_format)>`__
-   `.pcd <http://pointclouds.org/documentation/tutorials/pcd_file_format.php#pcd-file-format>`__
-   `.ply <https://en.wikipedia.org/wiki/PLY_(file_format)>`__

Reading
=======

.. automethod:: PyntCloud.from_file

.. code-block:: python

    from pyntcloud import PyntCloud
    my_point_cloud = PyntCloud.from_file("some_file.ply")
    
Writing
=======

.. automethod:: PyntCloud.to_file

.. code-block:: python

    # my_point_cloud is a PyntCloud instance
    my_point_cloud.to_file("out_file.obj", internals=["points", "mesh"])
    
Alternative ways for creating PyntClouds
========================================

Even though pyntcloud includes readers for some of the most common 3D file formats,
there are many other formats and sources where you can store point cloud data.

That's why although pyntcloud will include support for other file formats, it will
never cover all.

The good news are that as long as you can **load the data into Python**, you can create
a PyntCloud instance manually.

The key thing is to understand that you can't just plug in the raw data into the
PyntClud's constructor, there are some restrictions.

This restrictions are covered in :ref:`working-with-points`.

As long as you can adapt your data to this restrictions, you will be able
to construct a PyntCloud from formats that are not covered in *from_file*.

Some examples of manually constructing a PyntCloud:

ASCII files
===========

There are many formats englobed in this kind of files: .asc, .txt, .pts, ...

Normally, the first 3 columns represent the X,Y,Z coordinates of the point and
the rest of the columns represent some scalar field associated to that point
(Maybe R,G,B values, or Nx,Ny,Nz, etc).

To construct a PyntCloud from ascii files, you can use the pandas function 
`.read_csv <http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html>`__.

Check the linked documentation to explore all the possible arguments in order to
adjust them to read your ascii file.

As an example, given a *example.pts* file with this content:

.. code-block:: python

    8
    -0.037829 0.12794 0.004474
    -0.044779 0.128887 0.001904
    -0.068009 0.151244 0.037195
    -0.002287 0.13015 0.02322
    -0.022605 0.126675 0.007155
    -0.025107 0.125921 0.006242
    -0.03712 0.127449 0.001795
    0.033213 0.112692 0.027686
    
You can construct a PyntCloud as follows:

.. code-block:: python
    
    import pandas as pd
    from pyntcloud import PyntCloud
    
    points = pd.read_csv("example.pts", 
                         sep=" ",
                         header=0, 
                         names=["x","y","z"])
    
    cloud = PyntCloud(points)