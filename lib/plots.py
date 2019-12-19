# Import all of the basic libraries (you will always need these)
from matplotlib import pyplot as pl
import numpy as np
import pandas as pd

def InfiltrationPlot(state,grid):
    pl.figure(figsize=(10,5))
    pl.subplot(1,2,1)
    pl.plot(state['psi'].T,state['z'])
    pl.ylim(grid['ProfileDepth'],0)
    pl.ylabel('Depth below ground (m)',fontsize=13)
    pl.xlabel('Matric potential (m)',fontsize=13)
    pl.grid()

    pl.subplot(1,2,2)
    pl.plot(state['theta'].T,state['z'])
    pl.ylim(grid['ProfileDepth'],0)
    pl.xlabel('Volumetric water content (-)',fontsize=13)
    pl.grid()

def SimpleBalancePlot(ts):
    # Shift all fluxes half a step forward
    # Only plot the change in storage from the second step
    
    t=ts.index
    dt=t[1]-t[0]
    tm=t+dt/2.
    pl.plot(t[1:],ts['dS'].iloc[1:],label='dS')
    pl.plot(tm,ts['qI'],label='qI')
    pl.plot(tm,ts['qD'],label='qD')
    pl.plot(tm,(ts['qI']-ts['qD']),'.',label='Net flux')
    pl.legend()
    
def NumToDate(t,start):
    freq=(t[1]-t[0])
    if freq<1/24:
        freq='%.8fmin'%(freq*24*60)
    elif freq<1:
        freq='%.8fH'%(freq*24)
    else:
        freq='%.8fD'%(freq)
    return pd.date_range(start=start,freq=freq,periods=len(t))

def DateToNum(t):
    dd=t-t[0]
    return (dd.days+dd.seconds/86400.).values

