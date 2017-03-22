===================
Working with points
===================

A classic point cloud is just a set of points. 

In pyntcloud *points* is one of many attributes of the core class PyntCloud, althougt it's probably the most important.

This attribute is internally represented as a 
`pandas DataFrame <http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html>`__.

It is highly recommended to read the pandas DataFrame documentation in order to
understand what are the posibilitites for manipulating the point
cloud information that this entitie brings.

.. code-block:: python

    from pyntcloud import PyntCloud
    
    cloud = PyntCloud.from_file("test/data/filters/filters.ply")   
    
    cloud.points
    """
         x    y    z
    0  0.0  0.0  0.0
    1  0.1  0.1  0.1
    2  0.2  0.2  0.2
    3  0.5  0.5  0.5
    4  0.9  0.9  0.9
    5  1.0  1.0  1.0
    """

Restrictions
============

Two of the few restrictions that you will find in pyntcloud are related to the *points*
attribute.

-   *points* must be a pandas DataFrame

If you want to instantiate a PyntCloud using the constructor, you have to pass 
a pandas DataFrame as the *points* argument.

If you want to change the *points* argument, you have to change it for a new 
pandas DataFrame.

.. code-block:: python

    import numpy as np
    
    from pyntcloud import PyntCloud
    
    points = np.random.rand(1000, 3)
    
    cloud = PyntCloud(points)
    
    "TypeError: Points argument must be a DataFrame"
    
-   *points* must have 'x', 'y' and 'z' columns

The DataFrame that you use as *points* must have at least this 3 columns.

.. code-block:: python

    import numpy as np
    
    import pandas as pd
    
    from pyntcloud import PyntCloud
    
    points = pd.DataFrame(np.random.rand(1000, 3))
    
    cloud = PyntCloud(points)
    
    "ValueError: Points must have x, y and z coordinates"
    

    