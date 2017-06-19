import numpy as np
from stl import mesh
import pandas as pd

def read_stl(filename):
    stl = mesh.Mesh.from_file(filename)
    length1 = np.size(stl.x.flatten(),0)
    length2 = np.size(stl.normals[:,0])
    length3 = np.size(stl.v0.flatten())
    
    index1 = pd.RangeIndex(start=0,stop=length1)
    index2 = pd.RangeIndex(start=0,stop=length2)
    index3 = pd.RangeIndex(start=0,stop=length3)

    x = stl.x.flatten()
    y = stl.y.flatten()
    z = stl.z.flatten()

    nx = stl.normals[:,0]
    ny = stl.normals[:,1]
    nz = stl.normals[:,2]

    v0 = stl.v0.flatten()
    v1 = stl.v1.flatten()
    v2 = stl.v2.flatten()

    x = x.reshape(length1,1)
    y = y.reshape(length1,1)
    z = z.reshape(length1,1)

    nx = nx.reshape(length2,1)
    ny = ny.reshape(length2,1)
    nz = nz.reshape(length2,1)

    v0 = v0.reshape(length3,1)
    v1 = v1.reshape(length3,1)
    v2 = v2.reshape(length3,1)



    #data = pd.DataFrame([1,1],0,columns=['points'])
    data = {}
    data['points'] = pd.DataFrame(np.zeros([length1,3]),index=index1,columns=['x','y','z'])
    data['normals'] = pd.DataFrame(np.zeros([length2,3]),index=index2,columns=['nx','ny','nz'])
    data['mesh'] = pd.DataFrame(np.zeros([length3,3]),index=index3,columns=['v1','v2','v3'])
    

    data['points'].x = x
    data['points'].y = y  
    data['points'].z = z
    
    data['normals'].nx = nx
    data['normals'].ny = ny  
    data['normals'].nz = nz
    
    data['mesh'].v1 = v0
    data['mesh'].v2 = v1  
    data['mesh'].v3 = v2

    return data
