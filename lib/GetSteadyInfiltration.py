import numpy as np
from lib.vanGenuchten_numba import KFun

def GetSteadyInfiltration(pars,q):
    # Use mid-point search to find psi, where K(psi)=q. Search in logspace
    psiL=-3
    psiU=3
    errL=errfun(psiL,pars,q)
    errU=errfun(psiU,pars,q)
    errM=10
    c=0
#     print(c,errM,psiL,psiU)

    while np.abs(errM)>1e-10 and c < 100:
        psiM=(psiL+psiU)/2.
        errM=errfun(psiM,pars,q)
        if errM < 0.:
            psiL=psiM
            errL=errM
        else:
            psiU=psiM
            errU=errM
        c+=1
#         print(c,psiM,errM)
    if c == 100: print('Warning: reached %d iterations'%c)
    return -10**psiM

def errfun(psi,pars,q):
    return q-KFun(np.array([-10**psi]),pars)
