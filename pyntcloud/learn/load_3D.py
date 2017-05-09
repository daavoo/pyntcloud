from ..core_class import PyntCloud


def load_3D(path,
            n_sampling=10000,
            voxelize=True,
            voxel_mode="binary",
            target_size=(30, 30, 30)):
    """Load 3D data into numpy array, optionally voxelizing it.

    Parameters
    ----------
    path : srt
        Path to 3D file.

    n_sampling : int
        Number of points to be sampled in case the readed 3D data contains a mesh.

    voxelize : bool, optional (Default True)
        Indicates wheter the 3D data will be converted into voxelgrid or not.

    voxel_mode : {"binary", "density", "TDF"}, optional (Default "binary")
        The type of feature vector that will be generated from the voxelgrid.
        binary
            0 for empty voxels, 1 for occupied.
        density
            number of points inside voxel / total number of points.
        TDF
            Truncated Distance Function. Value between 0 and 1 indicating the distance
            between the voxel's center and the closest point. 1 on the surface,
            0 on voxels further than 2 * voxel side.

    target_size : [int, int, int], optional (Default [30, 30, 30])
        Dimensions of voxelgrid in case voxelize is True.

    Returns
    -------
    feature_vector : ndarray
        (target_size[0], target_size[1], target_size[2])

    Raises
    ------
    ValueError: if 3D format is not valid.

    """
    point_cloud = PyntCloud.from_file(path)

    if point_cloud.mesh is not None:
        point_cloud = PyntCloud(point_cloud.get_sample(
            "mesh_random_sampling", n=n_sampling))

    if voxelize:
        vgrid_id = point_cloud.add_structure("voxelgrid", x_y_z=target_size)
        voxelgrid = point_cloud.structures[vgrid_id]

        if voxel_mode == "binary":
            feature_vector = voxelgrid.get_feature_vector(mode="binary")
        elif voxel_mode == "density":
            feature_vector = voxelgrid.get_feature_vector(mode="density")
        elif voxel_mode == "TDF":
            feature_vector = voxelgrid.get_feature_vector(mode="TDF")
        else:
            raise ValueError("Unvalid mode; avaliable modes are: {}".format(
                {"binary", "density", "TDF"}))

        # add fake channel
        return feature_vector[None, ...]

    else:
        return point_cloud
