import numpy as np
from numba import jit
from lib.vanGenuchten_numba import KFun

@jit(nopython=True)
def InfiltrationFun(t,qIt,qI,psiT,dz,pars):
    # Upper boundary infiltration flux and runoff
    # Infiltration capacity such that psiT<=0 
    
    # Get Potential infiltration at the current time step
    PotentialInfiltration=np.interp(t,qIt,qI)

    # Surface saturation limited (max flux from Darcy's law):
    # Note, KFun always needs an array input, even if only a single item, and 
    # always writes output as an array. numba doesn't like zero-D arrays, so
    # when calculating a single value of K, convert to a float afterwards.
    KT=KFun(np.array([psiT]),pars)[0]
    InfiltrationCapacity=-KT*(psiT/dz*2.-1.)
#     Infiltration=InfiltrationCapacity
    
    # Actual infiltration flux:
    Infiltration=min(PotentialInfiltration,InfiltrationCapacity)
    
    return Infiltration
