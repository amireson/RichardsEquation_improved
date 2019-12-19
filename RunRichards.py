# Import all of the basic libraries (you will always need these)
from matplotlib import pyplot as pl
import numpy as np
import pandas as pd
import time

from numba import jit
from lib.MyNumba import MakeDictFloat

# Import a library that contains soil moisture properties and functions
from lib import vanGenuchten_numba as vg
from lib import Richards as re
from lib.plots import InfiltrationPlot
from lib.plots import SimpleBalancePlot

from lib import saveload as sl

IC=sl.json2dict('run/IC.json')
BC=sl.json2dict('run/BC.json')
grid=sl.json2dict('run/grid.json')
parsimport=sl.json2dict('run/pars.json')

pars=MakeDictFloat()
for k in parsimport:
    pars[k]=parsimport[k]

tic=time.time()
ts,state=re.runmodel(IC,BC,pars,grid)
print('runtime = %.1f seconds'%(time.time()-tic))

sl.save(ts,'run/ts')
sl.save(state,'run/state')
