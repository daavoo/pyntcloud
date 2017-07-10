.. _points:

======
Points
======

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

.. parsed-literal::
         x    y    z
    0  0.0  0.0  0.0
    1  0.1  0.1  0.1
    2  0.2  0.2  0.2
    3  0.5  0.5  0.5
    4  0.9  0.9  0.9
    5  1.0  1.0  1.0


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

.. parsed-literal::

    TypeError: Points argument must be a DataFrame

-   *points* must have 'x', 'y' and 'z' columns

The DataFrame that you use as *points* must have at least this 3 columns.

.. code-block:: python

    import numpy as np

    import pandas as pd

    from pyntcloud import PyntCloud

    points = pd.DataFrame(np.random.rand(1000, 3))

    cloud = PyntCloud(points)

.. parsed-literal::

    ValueError: Points must have x, y and z coordinates

Basic manipulation
==================

As mentioned above, the fact of having the points information in a pandas DataFrame
brings many possibilities regarding the analysis and manipulation of this data.

As you can read in Working with scalar fields, one of the key features of pyntcloud
is the flexibility that it offers regarding how you can add information and manipulate points.

You can quickly get statistical information about points with a single command:

.. code-block:: python

    from pyntcloud import PyntCloud

    cloud = PyntCloud.from_file("test/data/filters/filters.ply")

    cloud.points.describe()

.. parsed-literal::

                  x         y         z
    count  6.000000  6.000000  6.000000
    mean   0.450000  0.450000  0.450000
    std    0.423084  0.423084  0.423084
    min    0.000000  0.000000  0.000000
    25%    0.125000  0.125000  0.125000
    50%    0.350000  0.350000  0.350000
    75%    0.800000  0.800000  0.800000
    max    1.000000  1.000000  1.000000


You can use different plots to visualize the information in points:

.. code-block:: python

    cloud.points.boxplot()

.. image:: /images/boxplot.png

.. code-block:: python

    from pandas.tools.plotting import scatter_matrix

    scatter_matrix(cloud.points, diagonal="kde", figsize=(8,8))

.. image:: /images/scatter_matrix.png

You can perform operations over points like getting wich points are above some
"z" coordinate:

.. code-block:: python

    above_03 = cloud.points["z"] > 0.3
    above_03

.. parsed-literal::

    0    False
    1    False
    2    False
    3     True
    4     True
    5     True
    Name: x, dtype: bool


You can find more information about this kind of operations in Working with scalar
fields.

As mentioned above, to fully understad the manipulation possibilities that the
pandas DataFrame brings, is better to take a look at
`it's documentation <http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html>`__.
