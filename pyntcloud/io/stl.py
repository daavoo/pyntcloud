import numpy as np
from stl import mesh
import pandas as pd

def read_stl(filename):
    stl = mesh.Mesh.from_file(filename)
    length = np.size(stl.x.flatten(),0)

    index = pd.RangeIndex(start=0,stop=length)

    x = stl.x.flatten()
    y = stl.y.flatten()
    z = stl.z.flatten()

    x = x.reshape(length,1)
    y = y.reshape(length,1)
    z = z.reshape(length,1)
    #data = pd.DataFrame([1,1],0,columns=['points'])
    data = {}
    data['points'] = pd.DataFrame(np.zeros([length,3]),index=index,columns=['x','y','z'])
    
    data['points'].x = x
    data['points'].y = y  
    data['points'].z = z
    
    return data
