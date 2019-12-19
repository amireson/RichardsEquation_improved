import numpy as np
from numba import jit

@jit(nopython=True)
def PlantFun(psi,t,PEt,PE,z,dz,pars):
    # Root water uptake function, based on Feddes model
    
    PE=np.interp(t,PEt,PE)
    # Get root distribution:
    rd=np.exp(z/-pars['rootdepth'])
    
    # Get water stress:
    a=np.interp(psi,np.array([-1e6,-150,-4,-0.02,-0.01,1e6]),np.array([0,0,1,1,0,0]))
    
    # Uptake:
    Sp=PE*a*rd/np.sum(rd*dz+1e-30)
    
    return Sp

def AEfun(t,psi,PEt,PE,pars,dz,z):
    # Use root water uptake model to calculate Actual Evaporation
    
    AE=np.zeros(len(t))
    for i in range(len(t)):
        Sp=PlantFun(psi[i,:],t[i],PEt,PE,z,dz,pars)
        AE[i]=np.sum(Sp*dz)
    return AE
   
   
   