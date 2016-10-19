import os

from pyntcloud import PyntCloud

# just in case test are being runned from other directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))
sphere = PyntCloud.from_file('../data/sphere.ply')

def test_kdtree():
    
