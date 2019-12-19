# Import all of the basic libraries (you will always need these

# numpy/pandas
import numpy as np
import pandas as pd

# Import ODE solvers
from scipy.interpolate import interp1d
from scipy.integrate import odeint

# numba to speed up runtimes
from numba import jit
from lib.MyNumba import MakeDictFloat, MakeDictArray

# Import a library that contains soil moisture properties and functions
from lib.vanGenuchten_numba import thetaFun
from lib.vanGenuchten_numba import CFun
from lib.vanGenuchten_numba import KFun

# Import flux functions
# Read run options:
from lib import saveload as sl
BC=sl.json2dict('run/BC.json')
if BC['upper'].lower()=='runoff':
    from lib.InfiltrationFunRunoff import InfiltrationFun
    print("    Upper boundary condition: Runoff generated to prevent ponding")
elif BC['upper'].lower()=='norunoff':
    from lib.InfiltrationFunNoRunoff import InfiltrationFun
    print("    Upper boundary condition: zero runoff, 100% infiltration")
else:
    print('Warning: no upper boundary condition selected. Abort and try again')

if BC['lower'].lower()=='watertable':
    from lib.DrainageFunWaterTable import DrainageFun
    print("    Lower boundary condition: Fixed water table")
elif BC['lower'].lower()=='free':
    from lib.DrainageFunFreeDrainage import DrainageFun
    print("    Lower boundary condition: Free drainage")
elif BC['lower'].lower()=='noflow':
    from lib.DrainageFunNoFlow import DrainageFun
    print("    Lower boundary condition: No flow")
else:
    print('Warning: no lower boundary condition selected. Abort and try again')

from lib.PlantFunctions import PlantFun
from lib.PlantFunctions import AEfun

# Import other functions
from lib.GetSteadyInfiltration import GetSteadyInfiltration


# 
####################################################################################
#

# Function to run model:
def runmodel(IC,BC,pars,grid):
    # This block of code sets up and runs the model

    # Grid in space
    dz=grid['dz']
    ProfileDepth=grid['ProfileDepth']

    z=np.arange(dz/2.0,ProfileDepth,dz)
    n=z.size

    # Grid in time:
    t=grid['t']
    
    # Initial conditions
    if IC['type']=='SteadyInfiltration':
        psiInfiltration=GetSteadyInfiltration(pars,IC['value'])
        psi0=np.zeros(len(z))+psiInfiltration
        print("    Initial condition: steady-state infiltration profile")
    elif IC['type']=='Hydrostatic':
        psi0=z-grid['ProfileDepth']
        print("    Initial condition: hydrostatic profile")
    elif IC['type']=='Saturation':
        Se=IC['value']
        psi0=np.zeros(len(z))-(Se**(-1/pars['m'])-1)**(1/pars['n'])/pars['alpha']
        print("    Initial condition: specified saturation")
    elif IC['type']=='psi':
        psi0=IC['value']
        print("    Initial condition: specified matric potential")

    # Boundary conditions:
    qI=BC['qI']
    qIt=BC['qIt']
    PEt=BC['PEt']
    PE=BC['PE']
    
    
    # Solve and post process various model configurations:
    print("\nSolving Richards' Equation")
    psi=odeint(RichardsModelSimple,psi0,t,args=(dz,z,n,qIt,qI,PEt,PE,pars),ml=1,mu=1,mxstep=10000);
    ts,state=PostProcessSimple(t,z,psi,grid,IC,BC,pars)
    print("Model run successfully")

    return ts,state

# Richards equation solver:
@jit(nopython=True)
def RichardsModelSimple(psi,t,dz,z,n,qIt,qI,PEt,PE,pars): #,BC):
       
    # Basic properties:
    C=CFun(psi,pars)
   
    # initialize vectors:
    q=np.zeros(n+1)
    
    # Upper boundary: infiltration rate
    q[0]=InfiltrationFun(t,qIt,qI,psi[0],dz,pars)
            
    # Lower boundary
    q[n]=DrainageFun(pars,psi[-1],dz)
    
    # Internal nodes
    i=np.arange(0,n-1)
    Knodes=KFun(psi,pars)
    Kmid=(Knodes[i+1]+Knodes[i])/2.0
    
    j=np.arange(1,n)
    q[j]=-Kmid*((psi[i+1]-psi[i])/dz-1.0)
    
    # 
    Sp=PlantFun(psi,t,PEt,PE,z,dz,pars)
    
    # Continuity
    i=np.arange(0,n)
    dpsidt=(-(q[i+1]-q[i])/dz-Sp)/C
    
    return dpsidt

# Postprocess and save model outputs
def PostProcessSimple(tmod,z,psi,grid,IC,BC,pars):
    # Post process model output to get useful information

    # Get water content
    i,j=psi.shape
    theta=np.reshape(thetaFun(psi.flatten(),pars),(i,j))

    # Get total profile storage
    S=theta.sum(axis=1)*grid['dz']

    # Get change in storage [dVol]
    dS=np.zeros(S.size)
    dS[1:]=np.diff(S)/(tmod[1]-tmod[0])

    # Get infiltration flux
    qI=np.array([InfiltrationFun(tmod[i],BC['qIt'],BC['qI'],psi[i,0],grid['dz'],pars) for i in range(len(tmod))]).squeeze()
    
    # Get runoff flux
    PotI=np.interp(tmod,BC['qIt'],BC['qI'])
    runoff=PotI-qI

    # Get discharge flux
    qD=np.array([DrainageFun(pars,psiB,grid['dz']) for psiB in psi[:,-1]])
    
    # Get evaporation flux
    PE=np.interp(tmod,BC['PEt'],BC['PE'])
    AE=AEfun(tmod,psi,BC['PEt'],BC['PE'],pars,grid['dz'],z)
    
    state={}
    state['t']=tmod
    state['z']=z
    state['psi']=psi
    state['theta']=theta
    
    ts=pd.DataFrame(index=tmod)
    ts['qI']=qI
    ts['runoff']=runoff
    ts['qD']=qD
    ts['PE']=PE
    ts['AE']=AE
    ts['S']=S
    ts['dS']=dS

    # Print water balance to the screen:
    dt=tmod[1]-tmod[0]
    print('    Water balance information:')
    print('%-30s%.4f mm'%('Infiltration',np.sum(qI[1:])*dt))
    print('%-30s%.4f mm'%('Drainage',np.sum(qD[1:])*dt))
    print('%-30s%.4f mm'%('Actual evaporation',np.sum(AE[1:])*dt))
    print('%-30s%.4f mm'%('Potential evaporation',np.sum(PE[1:])*dt))
    print('%-30s%.4f mm'%('Change in storage',S[-1]-S[0]))
    print('%-30s%.4f mm'%('Balance',(np.sum(qI[1:]-qD[1:]-AE[1:])*dt-(S[-1]-S[0]))))

    return ts,state

