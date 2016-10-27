import os
import re

from pyntcloud import PyntCloud

# just in case test are being runned from other directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))
sphere = PyntCloud.from_file('../docs/data/sphere.ply')


def test_kdtree():

    sphere.add_structure('kdtree')
    sphere.add_structure('kdtree', leafsize=20)

    for n, k in enumerate(sphere.kdtrees):
        assert int(k.split("-")[-1]) == sphere.kdtrees[k].leafsize
    
    # check if unique-key system works
    sphere.add_structure('kdtree')
    assert len(sphere.kdtrees) == 2


def test_voxelgrid():

    sphere.add_structure('voxelgrid', x_y_z=[3,3,3])
    sphere.add_structure('voxelgrid', x_y_z=[4,5,6])

    n_voxels = [27, 120]

    for n, k in enumerate(sphere.voxelgrids):
        n = 1
        # LOL
        for x in re.findall("\d,\s\d,\s\d", k)[0].replace(" ", "").split(","):
            n*= int(x)
        assert sphere.voxelgrids[k].n_voxels == n
    
    sphere.add_structure('voxelgrid', x_y_z=[3,3,3])
    assert len(sphere.voxelgrids) == 2


def test_neighbourhood():

    sphere.add_structure('kdtree')
    sphere.add_structure('neighbourhood', kdtree="S-16")
    sphere.add_structure('neighbourhood', kdtree="S-16", k=3)

    for n, k in enumerate(sphere.neighbourhoods):

        assert int(k.split("-")[-1]) - 1 == sphere.neighbourhoods[k].distances.shape[1]
    
    sphere.add_structure('neighbourhood', kdtree="S-16")
    assert len(sphere.neighbourhoods) == 2
    
