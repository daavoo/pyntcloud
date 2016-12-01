#  HAKUNA MATATA

import numpy as np

class Sphere():

    def __init__(self, center=None, radius=None, normals=False):
        self.center = center
        self.radius= radius
        # for ransac
        self.k = 2 if normals else 4
    
    def from_four_points(self, points):
        pass