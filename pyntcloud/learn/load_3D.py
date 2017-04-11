from ..pyntcloud import PyntCloud

def load_3D(path, 
            n_sampling=None,
            voxelize=True,
            voxel_mode="binary",
            target_size=(30,30,30)):
    """Loads 3D data into numpy array, voxelizing it.

    Parameters
    ----------
    path : srt
        Path to 3D file.
    n_sampling : int
        Number of points to be sampled in case the readed 3D data contains a mesh.
    voxelize : bool, optional (Default True)
        Indicates wheter the 3D data will be converted into voxelgrid or not.
    voxel_mode : {"binary", "density", "tdf"}, optional (Default "binary")
        The type of feature vector that will be generated from the voxelgrid.
        binary : uint8
            0 for unnocupied voxels 1 for occupied
        density : float16
            n_points_in_voxel / n_total_points
        truncated : float16
            Value between 0 and 1 indicating the distance between the voxel's center and
            the closest point. 1 on the surface, 0 on voxels further than 2 * voxel side.            
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
    
    if "mesh" in point_cloud:
        if n_sampling is None:
            n_sampling = len(point_cloud["mesh"]) * 10

        point_cloud = PyntCloud(point_cloud.get_sample("mesh_random_sampling", n=n_sampling))
    
    if voxelize:
        vgrid_id = point_cloud.add_structure("voxelgrid", x_y_z=target_size)
        voxelgrid = point_cloud.structures[vgrid_id]
        
        if voxel_mode == "binary":
            feature_vector = binary_vector(v_grid, target_size)
        elif voxel_mode == "density":
            feature_vector = density_vector(v_grid, target_size)
        elif voxel_mode == "truncated":
            feature_vector = truncated_distance_function(point_cloud, centers, target_size, dimensions)
        else:
            raise ValueError("Unvalid mode; avaliable modes are: {}".format({"binary", "density", "truncated"}))
        
        return feature_vector
        
    else:
        return point_cloud

