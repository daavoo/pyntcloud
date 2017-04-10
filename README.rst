=========================
3D Point Clouds in Python
=========================

.. image:: /docs/images/pyntcloud_logo.png

Pyntcloud is a Python library for working with 3D point clouds.

It's currently under heavy development so you should expect API changes. Check Projects tab: https://github.com/daavoo/pyntcloud/projects/2

Check the documentation at: http://pyntcloud.readthedocs.io/en/latest/index.html

You can follow the quickstart bellow for a real-world example of using pyntcloud.

QuickStart
==========

It's our first day at the Jurassic Park Computer Vision Lab and our advisor has
asked us to solve the following problem:

We are given a 3D scene simulating the point clouds that are generated from a
lidar sensor on top of one of the Jurassic Park self-driving cars. 

Here is a view of the 3D scene:

.. image:: /docs/images/1.png

Although we will be working with only the parts of the scene that are visible from
the front of the car to simulate what the lidar sees.

Our task is to help the JP car chosing whether it should turn to the left, where
there is an apacible ankylosaurus, or right, where there is a hungry tyranosaurus.

----

Most of the pyntcloud's functionallity can be accesed by the core class: `PyntCloud`.

.. code-block:: python

    from pyntcloud import PyntCloud
    
And that is the only import we need for now.

Loading 3D data
---------------

The first thing we are going to do is load the 3D data into Python:

.. code-block:: python

    scene = PyntCloud.from_file("visible.ply")
    
And checking what is the information contained in it:

.. code-block:: python

    print(scene)
    """
    PyntCloud
    51777 points with 7 scalar fields
    99059 faces in mesh
    0 kdtrees
    0 octrees
    0 voxelgrids
    Centroid: -17.429340362548828, 7.901965618133545, 5.268535137176514
    Other attributes:  
    """

We notice that the file is actually a triangular mesh. 

Those lazy bastards from the desing deparment didn't convert the 3D model into 
a point cloud, wich is the real output from a lidar scanner.

3D point cloud from 3D mesh
---------------------------

Luckely we can convert a triangular mesh into a point cloud:

.. code-block:: python

    # sample 500000 points from the mesh
    sampled_points = scene.get_sample("mesh_random_sampling",
                                      n=500000,
                                      rgb=True,
                                      normals=True)
    
    # manually construcst a PyntCloud with those points
    scene = PyntCloud(sampled_points)

Check the result:

.. code-block:: python
    
    print(scene)
    """
    PyntCloud
    500000 points with 6 scalar fields
    0 faces in mesh
    0 kdtrees
    0 octrees
    0 voxelgrids
    Centroid: -10.083915710449219, 0.9554269313812256, 0.3894706070423126
    Other attributes:   
    """
        
And visualize the scene:

.. image:: /docs/images/2.gif

Floor segmentation
------------------

We are not interested in the points that compose the floor, so we will use 
`RANSAC <https://es.wikipedia.org/wiki/RANSAC>`__ to find the plane that contains 
those points:

.. code-block:: python
    
    scene.add_scalar_field("plane_fit", n_inliers_to_stop=len(scene.points)/30)
    
    print(scene.points.head())
    """
               x          y    z  red  green  blue   nx   ny   nz  is_plane
    0 -23.514395 -10.208544  0.0    0     85     0  0.0  0.0  1.0         1
    1 -21.890928  46.220840  0.0    0     85     0  0.0  0.0  1.0         1
    2 -21.945238 -43.863705  0.0    0     85     0  0.0  0.0  1.0         1
    3 -17.939890   4.941135  0.0    0     28     0  0.0  0.0  1.0         1
    4 -22.573780  44.184689  0.0    0     85     0  0.0  0.0  1.0         1
    """

And visualize the scene using the new scalar field:

.. image:: /docs/images/3.gif

Now we can use the `is_plane` scalar field to segment the point cloud:

.. code-block:: python
    
    not_floor = scene.points["is_plane"] != 1 
    
    scene.points = scene.points[not_floor]

And visualize the segmented point cloud:

.. image:: /docs/images/4.gif


WORK IN PROGRESS
