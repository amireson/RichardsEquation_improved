import numpy as np
from numba import jit

@jit(nopython=True)
def InfiltrationFun(t,qIt,qI,psiT=0,dz=0,pars=0):
    # Type 2 boundary
    qI=np.interp(t,qIt,qI)
    return qI

