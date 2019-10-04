=============================
Making point clouds fun again
=============================


.. image:: https://github.com/daavoo/pyntcloud/workflows/Python%20package/badge.svg
    :target: https://github.com/daavoo/pyntcloud/actions
    :alt: Github Actions Status

.. image:: https://mybinder.org/badge.svg
    :target: https://mybinder.org/v2/gh/daavoo/pyntcloud/master
    :alt: Start in Binder

.. image:: https://img.shields.io/pypi/v/pyntcloud
    :target: https://https://pypi.org/project/pyntcloud/
    :alt: Pypi

.. image:: https://raw.githubusercontent.com/daavoo/pyntcloud/master/docs/images/pyntcloud_logo.png
    :alt: pyntcloud logo

**pyntcloud** is a Python **3** library for working with 3D point clouds leveraging the power of the Python scientific stack.

- Examples_ (We encourage you to try the examples without installation launching `Binder <https://mybinder.org/v2/gh/daavoo/pyntcloud/master>`_.)
- Documentation_

.. _Examples: https://github.com/daavoo/pyntcloud/tree/master/examples
.. _Documentation: http://pyntcloud.readthedocs.io/en/latest/

.. code-block:: bash

    pip install pyntcloud

Quick Overview
==============

You can access most of pyntcloud's functionality from its core class: PyntCloud.

With PyntCloud you can perform complex 3D processing operations with minimum lines of
code. For example you can:

- Load a PLY point cloud from disk.
- Add 3 new scalar fields by converting RGB to HSV.
- Build a grid of voxels from the point cloud.
- Build a new point cloud keeping only the nearest point to each occupied voxel center.
- Save the new point cloud in numpy's NPZ format.

With the following concise code:

.. code-block:: python

    from pyntcloud import PyntCloud

    cloud = PyntCloud.from_file("some_file.ply")

    cloud.add_scalar_field("hsv")

    voxelgrid_id = cloud.add_structure("voxelgrid", n_x=32, n_y=32, n_z=32)

    new_cloud = cloud.get_sample("voxelgrid_nearest", voxelgrid_id=voxelgrid_id, as_PyntCloud=True)

    new_cloud.to_file("out_file.npz")

Integration with other libraries
================================

pyntcloud offers seamless integration with other 3D processing libraries.

You can create / convert PyntCloud instances from / to many 3D processing libraries using the `from_instance` / `to_instance` methods:

- `Open3D <https://www.open3d.org>`_

.. code-block:: python

    import open3d as o3d
    from pyntcloud import PyntCloud

    # FROM Open3D
    original_triangle_mesh = o3d.io.read_triangle_mesh("diamond.ply")
    cloud = PyntCloud.from_instance("open3d", original_triangle_mesh)
    assert cloud.mesh is not None
    assert np.allclose(cloud.mesh.values, original_triangle_mesh.triangles)
    assert np.allclose(cloud.xyz, original_triangle_mesh.vertices)
    assert {'red', 'green', 'blue'}.issubset(cloud.points.columns)
    assert np.allclose(cloud.points[['red', 'green', 'blue']].values / 255., original_triangle_mesh.vertex_colors)
    assert {'nx', 'ny', 'nz'}.issubset(cloud.points.columns)
    assert np.allclose(cloud.points[['nx', 'ny', 'nz']].values,  original_triangle_mesh.vertex_normals)

    # TO Open3D
    cloud = PyntCloud.from_file("diamond.ply")
    converted_triangle_mesh = cloud.to_instance("open3d", mesh=True)  # mesh=True by default
    assert isinstance(converted_triangle_mesh, o3d.geometry.TriangleMesh)
    assert np.allclose(cloud.xyz, converted_triangle_mesh.vertices)
    assert np.allclose(cloud.mesh.values, converted_triangle_mesh.triangles)

- `PyVista <https://docs.pyvista.org>`_

.. code-block:: python

    import pyvista as pv
    from pyntcloud import PyntCloud

    # FROM PyVista
    original_point_cloud = pv.read("diamond.ply")
    cloud = PyntCloud.from_instance("pyvista", original_point_cloud)
    assert np.allclose(cloud.xyz, original_point_cloud.points)
    assert {'red', 'green', 'blue'}.issubset(cloud.points.columns)
    assert np.allclose(cloud.points[['red', 'green', 'blue']].values, original_point_cloud.point_arrays["RGB"])
    assert {'nx', 'ny', 'nz'}.issubset(cloud.points.columns)
    assert np.allclose(cloud.points[['nx', 'ny', 'nz']].values,  original_point_cloud.point_arrays["Normals"])

    # TO PyVista
    cloud = PyntCloud.from_file("diamond.ply")
    converted_triangle_mesh = cloud.to_instance("open3d", mesh=True)
    assert isinstance(converted_triangle_mesh, pv.PolyData)
    assert np.allclose(cloud.xyz, converted_triangle_mesh.points)
    assert np.allclose(cloud.mesh.values, converted_triangle_mesh.faces[:, 1:])

