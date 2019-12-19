from numba import jit
import numpy as np
from lib.vanGenuchten_numba import KFun

@jit(nopython=True)
def DrainageFun(pars,psiB,dz):
    # Free drainage
    # Note, KFun always needs an array input, even if only a single item, and 
    # always writes output as an array. numba doesn't like zero-D arrays, so
    # when calculating a single value of K, convert to a float afterwards.
    KBot=KFun(np.array([psiB]),pars)[0]
    qD=KBot
    return qD
