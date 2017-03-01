
import numpy as np

def eigen_sum(ev):
    return [ev[:,0] + ev[:,1] + ev[:,2]]

def omnivariance(ev):
    return [(ev[:,0] * ev[:,1] * ev[:,2]) ** (1/3)]

def eigenentropy(ev):
    result = np.zeros(ev.shape[0])
    for i in range(3):
        result += ev[:,i] * np.log(ev[:,i])
    return [-result]

def anisotropy(ev):
    return [(ev[:,0] - ev[:,2]) / ev[:,0]]

def planarity(ev):
    return [(ev[:,1] - ev[:,2]) / ev[:,0]]

def linearity(ev):
    return [(ev[:,0] - ev[:,1]) / ev[:,0]]

def curvature(ev):
    return [ev[:,2] / (ev[:,0] + ev[:,1] + ev[:,2])]

def sphericity(ev):
    return [ev[:,2] / ev[:,0]]
