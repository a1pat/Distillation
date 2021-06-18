# -*- coding: utf-8 -*-
"""
Simulate the distillation column in Exampl 8.11 of Foust et al's
textbook.
"""

import numpy as np
import scipy
import pandas as pd
import matplotlib.pyplot as plt
#%matplotlib inline
#from sim_utils import map_var_to_unit1, map_eqn_to_unit1, process_eqns, get_info
from sim_utils import *

from unit import Unit
from stream import Stream
from mixer import Mixer
from tray import Tray
from connector import Connector
from specify import Specify
from simplecolumn import SimpleColumn


    


N_COMPS = 5

unit_dict = dict()

# instantiate the required objects

condensate = Stream(n_comps=N_COMPS, name='Condensate')
reflux = Stream(n_comps=N_COMPS, name='Reflux')
top_product = Stream(n_comps=N_COMPS, name='Top product')
bottoms = Stream(n_comps=N_COMPS, name='Bottoms')
vapor_reboil = Stream(n_comps=N_COMPS, name='Vapor reboil')
bottom_product = Stream(n_comps=N_COMPS, name='Bottom product')
feed = Stream(n_comps=N_COMPS, name='LiquidFeed')
condenser = Mixer(streams_in=[condensate], 
                  streams_out=[reflux, top_product], 
                  name='Condenser')
reboiler = Mixer(streams_in=[bottoms], 
                 streams_out=[vapor_reboil, bottom_product], 
                 name='Reboiler')
feed_flow_spec = Specify(flow=True, stream=feed, value=100)
feed_temp_spec = Specify(temperature=True, stream=feed, value=100)
feed_ic4_spec = Specify(fraction=True, stream=feed, comp_num=0, value=0.1)
feed_nc4_spec = Specify(fraction=True, stream=feed, comp_num=1, value=0.3)
feed_ic5_spec = Specify(fraction=True, stream=feed, comp_num=2, value=0.2)
feed_nc5_spec = Specify(fraction=True, stream=feed, comp_num=3, value=0.3)
feed_nc6_spec = Specify(fraction=True, stream=feed, comp_num=4, value=0.1)
reflux_flow_spec = Specify(flow=True, stream=reflux, value=120)
vapor_reboil_flow_spec = Specify(flow=True, stream=vapor_reboil, value=160)
top_product_flow_spec = Specify(flow=True, stream=top_product, value=40)
foust_8_11 = SimpleColumn(n_trays=15, feed_tray=7, 
                          feed_stream_liq=feed, 
                          reflux=reflux, 
                          vapor_reboil=vapor_reboil, 
                          condensate = condensate,
                          bottoms = bottoms,
                          pressure=45, 
                          tray_efficiency=1,
                          name='foust_8_11')
tray_temp_spec_bot = Specify(temperature=True, stream=foust_8_11.trays[3].liq_stream_out, value=155)
tray_temp_spec_top = Specify(temperature=True, stream=foust_8_11.trays[10].liq_stream_out, value=100)

# add only the objects used in the model to the dict

unit_dict['condensate'] = condensate
unit_dict['reflux'] = reflux
unit_dict['top_product'] = top_product
unit_dict['bottoms'] = bottoms
unit_dict['vapor_reboil'] = vapor_reboil
unit_dict['bottom_product'] = bottom_product
unit_dict['feed'] = feed
unit_dict['condenser'] = condenser
unit_dict['reboiler'] = reboiler
unit_dict['feed_flow_spec'] = feed_flow_spec
unit_dict['feed_temp_spec'] = feed_temp_spec
unit_dict['feed_ic4_spec'] = feed_ic4_spec
unit_dict['feed_nc4_spec'] = feed_nc4_spec
unit_dict['feed_ic5_spec'] = feed_ic5_spec
unit_dict['feed_nc5_spec'] = feed_nc5_spec
unit_dict['feed_nc6_spec'] = feed_nc6_spec
unit_dict['column'] = foust_8_11

#unit_dict['reflux_flow_spec'] = reflux_flow_spec
#unit_dict['top_product_flow_spec'] = top_product_flow_spec
#unit_dict['vapor_reboil_flow_spec'] = vapor_reboil_flow_spec
unit_dict['tray_temp_spec_bot'] = tray_temp_spec_bot
unit_dict['tray_temp_spec_top'] = tray_temp_spec_top



#print(reflux)
#print(reboiler)
#print(foust_8_11.unit_dict['foust_8_11CondensateConnector'])
#print(foust_8_11)
#print(feed_flow_spec)
#print(foust_8_11.unit_dict['foust_8_11Tray0'])


n_eqns = 0
for u in unit_dict:
    n_eqns += unit_dict[u].num_eqns()
    
n_vars = 0
for u in unit_dict:
    n_vars += unit_dict[u].num_vars()
    
# check if the number of equations is equal to the number of unknown variables
assert n_eqns == n_vars, '{} equations and {} unknown variables'.format(n_eqns, n_vars)

# initialize solver varaibles
#xvar = np.ones(n_vars, dtype=np.float64) * 100
xvar = get_unit_vars(unit_dict)
#print('initial guess')
#print(xvar)

# map solver variables to model variables
map_var_to_unit1(xvar, unit_dict)
# initialize solver residuals
eqns = np.ones(n_vars, dtype=np.float64)
# map solver residuals to model residuals
map_eqn_to_unit1(eqns, unit_dict)

# solve model equations

#x_solution = scipy.optimize.fsolve(process_eqns, xvar, args=(unit_dict, eqns))
#print(type(x_solution))

#x_solution, ier = scipy.optimize.leastsq(process_eqns, xvar, args=(unit_dict, eqns))
#print(type(x_solution))
#print('exited leastsq with ier = {}'.format(ier))

x_solution = scipy.optimize.root(process_eqns, xvar, args=(unit_dict, eqns), method='lm')
print(type(x_solution))
print(type(x_solution['x']))
print('success: {}'.format(x_solution['success']))
x_solution = x_solution['x']

#print(x_solution)

# map solver solution to model variables
map_var_to_unit1(x_solution, unit_dict)
# map solver residuals to model residuals
map_eqn_to_unit1(eqns, unit_dict)
# print residual SSE
print('sum of squares of residuals: {}'.format(np.sum(np.square(eqns))))

# get column profile
foust_profile = foust_8_11.profile()
# print temperature, liquid flow and vapor flow column profiles
print(foust_profile[['T', 'L', 'V']])
# print all column profiles
print(foust_profile)
#print(top_product_flow_spec)

#with open('open_loop.txt','a') as f:
#    f.write('\n\n\n')
#    f.write(str(x_solution))
#    f.write(get_info(unit_dict))
#    f.close()

# uncomment the following if you want plots of the temperature and liquid fraction profiles
#plt.figure()
#plt.plot(foust_profile['T'], foust_profile['tray_num'], '-')
#plt.xlabel('temperature')
#plt.ylabel('tray number')
#plt.grid(axis='both')

#plt.figure()
#plt.plot(foust_profile['x0'], foust_profile['tray_num'], '-')
#plt.plot(foust_profile['x1'], foust_profile['tray_num'], '-')
#plt.plot(foust_profile['x2'], foust_profile['tray_num'], '-')
#plt.plot(foust_profile['x3'], foust_profile['tray_num'], '-')
#plt.plot(foust_profile['x4'], foust_profile['tray_num'], '-')
#plt.xlabel('fraction')
#plt.ylabel('tray number')
#plt.grid(axis='both')
#plt.legend(['ic4','nc4','ic5','nc5','nc6'])
