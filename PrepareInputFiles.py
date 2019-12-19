# Script to prepare input data for three simple model runs

import numpy as np
from lib.MyNumba import MakeDictFloat
from lib import vanGenuchten_numba as vg
from lib import saveload as sl

import os
os.system('mkdir run001')
os.system('mkdir run002')
os.system('mkdir run003')

# CASE 1: ### Simple model run with constant boundary conditions

# Choose run configuration - steady or dynamic boundaries, with/without plant uptake:
# Set soil properties:
pars=vg.SiltLoamGE3()
pars['rootdepth']=0.2

# Set time and space grid:
t=np.arange(0,11)
grid={}
grid['t']=t
grid['dz']=0.05
grid['ProfileDepth']=5.

# Initial conditions: Choose from options
IC={}
# IC['type']='Hydrostatic'
IC['type']='SteadyInfiltration'
IC['value']=0.001

# Boundary conditions: Choose from options
BC={}
BC['qIt']=np.array([0,1e6])
BC['qI']=np.array([0.05,0.05])
BC['PEt']=np.array([0.0,1e6])
BC['PE']=np.array([0.,0.])

BC['upper']='NoRunoff'
BC['lower']='NoFlow'

fn='run001'
sl.dict2json(grid,fn+'/grid.json')
sl.dict2json(IC,fn+'/IC.json')
sl.dict2json(BC,fn+'/BC.json')
parsimport={}
for k in pars:
    parsimport[k]=pars[k]
sl.dict2json(parsimport,fn+'/pars.json')


# CASE 2: ### Same as above, but in dynamic model configuration (slower, but can handle time series input)

# Choose run configuration - steady or dynamic boundaries, with/without plant uptake:
# Set soil properties:
pars=vg.SiltLoamGE3()
pars['rootdepth']=0.2

# Set time and space grid:
t=np.arange(0,11)
grid={}
grid['t']=t
grid['dz']=0.05
grid['ProfileDepth']=5.

# Initial conditions: Choose from options
IC={}
# IC['type']='Hydrostatic'
IC['type']='SteadyInfiltration'
IC['value']=0.01

# Boundary conditions: Choose from options
BC={}
BC['qIt']=np.array([0.,2.,2.01,1e6])
BC['qI']=np.array([0.05,0.05,0.,0.])
BC['PEt']=np.array([0.0,1e6])
BC['PE']=np.array([0.,0.])

BC['upper']='NoRunoff'
BC['lower']='Free'

fn='run002'
sl.dict2json(grid,fn+'/grid.json')
sl.dict2json(IC,fn+'/IC.json')
sl.dict2json(BC,fn+'/BC.json')
parsimport={}
for k in pars:
    parsimport[k]=pars[k]
sl.dict2json(parsimport,fn+'/pars.json')


# CASE 3: ### One calendar year, plant and runoff generation

# Choose run configuration - steady or dynamic boundaries, with/without plant uptake:

# Set soil properties:
pars=vg.SiltLoamGE3()
pars['rootdepth']=0.2

# Set time and space grid:http://localhost:8888/notebooks/RunRichards.ipynb#
t=np.arange(365) #pd.date_range('1-Jan-2018',periods=365,freq='D')
grid={}
grid['t']=t
grid['dz']=0.05
grid['ProfileDepth']=5.

# Initial conditions: Choose from options
IC={}
IC['type']='Hydrostatic'
# IC['type']='SteadyInfiltration'
IC['value']=0.001

# Boundary conditions: Choose from options
PE=(1-np.cos(np.arange(365)/365*2*np.pi))/1000.
P=np.zeros(365)+0.001

BC={}
BC['qIt']=np.arange(365)
BC['qI']=P
BC['PEt']=np.arange(365)
BC['PE']=PE

BC['upper']='Runoff'
BC['lower']='WaterTable'

fn='run003'
sl.dict2json(grid,fn+'/grid.json')
sl.dict2json(IC,fn+'/IC.json')
sl.dict2json(BC,fn+'/BC.json')
parsimport={}
for k in pars:
    parsimport[k]=pars[k]
sl.dict2json(parsimport,fn+'/pars.json')

