from numba import jit
import numpy as np
from lib.vanGenuchten_numba import KFun

@jit(nopython=True)
def DrainageFun(pars,psiB,dz):
    # Type 1 boundary
    # Note, KFun always needs an array input, even if only a single item, and 
    # always writes output as an array. numba doesn't like zero-D arrays, so
    # when calculating a single value of K, convert to a float afterwards.
    KBot=KFun(np.zeros(1),pars)[0]
    qD=-KBot*((-psiB)/dz*2-1.0)    
    return qD
