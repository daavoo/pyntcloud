# Making point clouds fun again

![pyntcloud logo](https://raw.githubusercontent.com/daavoo/pyntcloud/master/docs/images/pyntcloud_logo.png)


**pyntcloud** is a Python library for working with 3D point clouds leveraging the power of the Python scientific stack.

- [Examples](https://github.com/daavoo/pyntcloud/tree/master/examples).
- [Documentation](http://pyntcloud.readthedocs.io/en/latest/)

## Installation

```bash
pip install pyntcloud
```

## Quick Overview

You can access most of pyntcloud's functionality from its core class: PyntCloud.

With PyntCloud you can perform complex 3D processing operations with minimum lines of
code. For example you can:

- Load a PLY point cloud from disk.
- Add 3 new scalar fields by converting RGB to HSV.
- Build a grid of voxels from the point cloud.
- Build a new point cloud keeping only the nearest point to each occupied voxel center.
- Save the new point cloud in numpy's NPZ format.

With the following concise code:

```python
from pyntcloud import PyntCloud

cloud = PyntCloud.from_file("some_file.ply")

cloud.add_scalar_field("hsv")

voxelgrid_id = cloud.add_structure("voxelgrid", n_x=32, n_y=32, n_z=32)

new_cloud = cloud.get_sample("voxelgrid_nearest", voxelgrid_id=voxelgrid_id, as_PyntCloud=True)

new_cloud.to_file("out_file.npz")
```

## Integration with other libraries

pyntcloud offers seamless integration with other 3D processing libraries.

You can create / convert PyntCloud instances from / to many 3D processing libraries using the `from_instance` / `to_instance` methods:

- [Open3D](https://www.open3d.org)

```python
import open3d as o3d
from pyntcloud import PyntCloud

# FROM Open3D
original_triangle_mesh = o3d.io.read_triangle_mesh("diamond.ply")
cloud = PyntCloud.from_instance("open3d", original_triangle_mesh)

# TO Open3D
cloud = PyntCloud.from_file("diamond.ply")
converted_triangle_mesh = cloud.to_instance("open3d", mesh=True)  # mesh=True by default
```

- [PyVista](https://docs.pyvista.org)

```python
import pyvista as pv
from pyntcloud import PyntCloud

# FROM PyVista
original_point_cloud = pv.read("diamond.ply")
cloud = PyntCloud.from_instance("pyvista", original_point_cloud)

# TO PyVista
cloud = PyntCloud.from_file("diamond.ply")
converted_triangle_mesh = cloud.to_instance("pyvista", mesh=True)
```
