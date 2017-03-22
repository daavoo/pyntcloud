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
    my_point_cloud.to_file("out_file.obj")
    
Alternative ways for creating PyntClouds
========================================


