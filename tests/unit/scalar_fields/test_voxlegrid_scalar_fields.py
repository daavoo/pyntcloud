import pytest

import numpy as np

from pyntcloud.scalar_fields.voxelgrid import (
    EuclideanClusters,
    VoxelgridScalarField,
    VoxelN,
    VoxelX,
    VoxelY,
    VoxelZ
)


@pytest.mark.parametrize("voxelgrid_id", [
    "FOO",
    "V([2, 2, 3],None,True)",
    "V([2, 2, 2],True,True))",
    "V([2, 2, 2],None,False)",
    "V([2, 2, 2])",
    "V(None,True)"
])
@pytest.mark.usefixtures("pyntcloud_with_voxelgrid_and_voxelgrid_id")
def test_VoxelgridScalarField_raises_KeyError_if_id_is_not_valid(pyntcloud_with_voxelgrid_and_voxelgrid_id, voxelgrid_id):
    cloud, true_id = pyntcloud_with_voxelgrid_and_voxelgrid_id
    scalar_field = VoxelgridScalarField(
        pyntcloud=cloud,
        voxelgrid_id=voxelgrid_id)
    with pytest.raises(KeyError):
        scalar_field.extract_info()


@pytest.mark.parametrize("scalar_field_class, min_val, max_val", [
    (
        VoxelN,
        0,
        4 * 4 * 4
    ),
    (
        VoxelX,
        0,
        4
    ),
    (
        VoxelY,
        0,
        4
    ),
    (
        VoxelZ,
        0,
        4
    ),
])
@pytest.mark.usefixtures("pyntcloud_with_voxelgrid_and_voxelgrid_id")
def test_VoxelgridScalarField_bounds(pyntcloud_with_voxelgrid_and_voxelgrid_id, scalar_field_class, min_val, max_val):
    cloud, voxelgrid_id = pyntcloud_with_voxelgrid_and_voxelgrid_id
    scalar_field = scalar_field_class(
        pyntcloud=cloud,
        voxelgrid_id=voxelgrid_id)
    scalar_field.extract_info()
    with np.errstate(divide='ignore', invalid='ignore'):
        scalar_field.compute()
    scalar_field_values = next(iter(scalar_field.to_be_added.values()))
    assert all(scalar_field_values >= min_val)
    assert all(scalar_field_values <= max_val)


@pytest.mark.usefixtures("pyntcloud_with_clusters_and_voxelgrid_id")
def test_EuclideanClusters_values(pyntcloud_with_clusters_and_voxelgrid_id):
    cloud, voxelgrid_id = pyntcloud_with_clusters_and_voxelgrid_id
    scalar_field = EuclideanClusters(
        pyntcloud=cloud,
        voxelgrid_id=voxelgrid_id)
    scalar_field.extract_info()
    with np.errstate(divide='ignore', invalid='ignore'):
        scalar_field.compute()
    scalar_field_values = next(iter(scalar_field.to_be_added.values()))
    assert all(scalar_field_values[:5] != scalar_field_values[5:])
