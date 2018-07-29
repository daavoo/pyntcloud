from pyntcloud.ransac.samplers import VoxelgridRansacSampler


def test_voxelgrid_sampler_return_points_in_the_same_voxel(pyntcloud_with_rgb_and_normals):
    points = pyntcloud_with_rgb_and_normals.xyz

    sampler = VoxelgridRansacSampler(points=points, k=2, size_x=0.5)

    sample = sampler.get_sample()

    assert sample[0][0] - sample[1][0] < 0.5
