#  HAKUNA MATATA

"""
Geometric functions for managing pointclouds

"""

import numpy as np
   

def Rx(angle, degrees=True):
    """ 
    """
    if degrees:
        
        cx = np.cos(np.deg2rad(angle))
        sx = np.sin(np.deg2rad(angle))
        
    else:
        
        cx = np.cos(angle)
        sx = np.sin(angle)
        
    Rx = np.array(
    [[1  , 0  , 0  , 0  ],
     [0  , cx , sx , 0  ],
     [0  , -sx, cx , 0  ],
     [0  , 0  , 0  , 1  ]]
    )
    
    return Rx
    
    
def Ry(angle, degrees=True):
    
    if degrees:
        
        cy = np.cos(np.deg2rad(angle))
        sy = np.sin(np.deg2rad(angle))
        
    else:
        
        cy = np.cos(angle)
        sy = np.sin(angle)
        
    Ry = np.array(
    [[cy , 0  , -sy, 0  ],
     [0  , 1  , 0  , 0  ],
     [sy , 0  , cy , 0  ],
     [0  , 0  , 0  , 1  ]]
    )
    
    return Ry
    
    
def Rz(angle, degrees=True):
        
    if degrees:
        
        cz = np.cos(np.deg2rad(angle))
        sz = np.sin(np.deg2rad(angle))
        
    else:
        
        cz = np.cos(angle)
        sz = np.sin(angle)
        
    Rz = np.array(
    [[cz , sz , 0  , 0  ],
     [-sz, cz , 0  , 0  ],
     [0  , 0  , 1  , 0  ],
     [0  , 0  , 0  , 1  ]]
    )
        
    return Rz
    
    
def T(tx, ty, tz):
    
    T = np.array(
    [[1  , 0  , 0  , 0  ],
     [0  , 1  , 0  , 0  ],
     [0  , 0  , 1  , 0  ],
     [tx , ty , tz , 1  ]]
    )
    
    return T

def S(sx, sy, sz):
    
    S = np.array(
    [[sx , 0  , 0  , 0  ],
     [0  , sy , 0  , 0  ],
     [0  , 0  , sz , 0  ],
     [0  , 0  , 0  , 1  ]]
    )
    
    return S
