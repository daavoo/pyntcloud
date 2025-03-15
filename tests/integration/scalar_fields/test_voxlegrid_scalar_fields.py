import pytest


@pytest.mark.parametrize(
    "scalar_field_name, min_val, max_val",
    [
        ("voxel_n", 0, 4 * 4 * 4),
        ("voxel_x", 0, 4),
        ("voxel_y", 0, 4),
        ("voxel_z", 0, 4),
    ],
)
@pytest.mark.usefixtures("pyntcloud_with_voxelgrid_and_voxelgrid_id")
def test_voxelgrid_scalar_fields_bounds(
    pyntcloud_with_voxelgrid_and_voxelgrid_id, scalar_field_name, min_val, max_val
):
    cloud, voxelgrid_id = pyntcloud_with_voxelgrid_and_voxelgrid_id
    scalar_field = cloud.add_scalar_field(scalar_field_name, voxelgrid_id=voxelgrid_id)
    scalar_field_values = cloud.points[scalar_field].values
    assert all(scalar_field_values >= min_val)
    assert all(scalar_field_values <= max_val)


@pytest.mark.usefixtures("pyntcloud_with_clusters_and_voxelgrid_id")
def test_euclidean_clusters_values(pyntcloud_with_clusters_and_voxelgrid_id):
    cloud, voxelgrid_id = pyntcloud_with_clusters_and_voxelgrid_id
    scalar_field = cloud.add_scalar_field(
        "euclidean_clusters", voxelgrid_id=voxelgrid_id
    )
    scalar_field_values = cloud.points[scalar_field].values
    assert all(scalar_field_values[:5] != scalar_field_values[5:])
