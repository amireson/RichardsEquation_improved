from numba import jit
import numpy as np
from lib.vanGenuchten_numba import KFun

@jit(nopython=True)
def DrainageFun(pars,psiB,dz):

    qD=0.
    return qD
