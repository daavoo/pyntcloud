![pyntcloud Logo](docs/data/pyntcloud.png)
# 3D Point Clouds in Python

Pyntcloud is a Python library for working with 3D point clouds.

## DOCUMENTATION
Jupyter notebook-based documentation with interactive tutorials and examples.

### Introduction
Accurate [3D point clouds](https://en.wikipedia.org/wiki/Point_cloud) can (easily and cheaply) be adquired nowdays from different sources. For example:

- RGB-D devices: [Google Tango](http://get.google.com/tango/), [Microsoft Kinect](https://developer.microsoft.com/en-us/windows/kinect), etc.
- [Lidar](https://en.wikipedia.org/wiki/Lidar).
- [3D reconstruction from multiple images](https://en.wikipedia.org/wiki/3D_reconstruction_from_multiple_images).


The aim of [pyntcloud](https://github.com/daavoo/pyntcloud) is to provide a way to work with 3D point clouds using Python in a clear, simple and fluent way.

Here you can find a quick introduction to the two main concepts on wich this library is based:

#### [What is a point cloud](docs/Introduction/what_is_a_point_cloud.ipynb)
#### [What is a PyntCloud](docs/Introduction/what_is_a_PyntCloud.ipynb)

### Reading and Writing point clouds
In order to work with point clouds we need to be able to read and write point cloud data, so let`s check how we can do this in pyntcloud:

#### [PyntCloud I/O](docs/Reading and Writing/from_file&to_file.ipynb)
#### [Supported file formats](docs/Reading and Writing/supported_file_formats.ipynb)

### Working with scalar fields
Most of the usefull information in a point cloud is associate with it's scalar fields. Here we well see how to work scalar fields in pyntcloud.

#### [Adding scalar fields](docs/Scalar Fields/adding_scalar_fields.ipynb)
#### [Avaliable scalar fields](docs/Scalar Fields/avaliable_scalar_fields.ipynb)

## SAMPLE DATA 

Inside the folder `docs/data` you can find examples of point clouds in different formats.

## INSTALATION

Version 0.1 will be reslased soon.

Recommended instalation for now:

```
git clone https://github.com/daavoo/pyntcloud.git

cd pyntcloud

python setup.py develop
```

