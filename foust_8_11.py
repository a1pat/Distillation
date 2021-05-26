# -*- coding: utf-8 -*-
"""
Simulate the distillation column in Exampl 8.11 of Foust et al's
textbook.
"""

import numpy as np
from scipy.optimize import fsolve
import pandas as pd
import matplotlib.pyplot as plt
#%matplotlib inline
from sim_utils import map_var_to_unit1, map_eqn_to_unit1, process_eqns

from unit import Unit
from stream import Stream
from mixer import Mixer
from tray import Tray
from connector import Connector
from specify import Specify
from simplecolumn import SimpleColumn


N_COMPS = 5

unit_dict = dict()

condensate = Stream(n_comps=N_COMPS, name='Condensate')
reflux = Stream(n_comps=N_COMPS, name='Reflux')
top_product = Stream(n_comps=N_COMPS, name='Top product')
bottoms = Stream(n_comps=N_COMPS, name='Bottoms')
vapor_reboil = Stream(n_comps=N_COMPS, name='Vapor reboil')
bottom_product = Stream(n_comps=N_COMPS, name='Bottom product')
feed = Stream(n_comps=N_COMPS, name='LiquidFeed')

unit_dict['condensate'] = condensate
unit_dict['reflux'] = reflux
unit_dict['top_product'] = top_product
unit_dict['bottoms'] = bottoms
unit_dict['vapor_reboil'] = vapor_reboil
unit_dict['bottom_product'] = bottom_product
unit_dict['feed'] = feed

condenser = Mixer(streams_in=[condensate], 
                  streams_out=[reflux, top_product], 
                  name='Condenser')

reboiler = Mixer(streams_in=[bottoms], 
                 streams_out=[vapor_reboil, bottom_product], 
                 name='Reboiler')

unit_dict['condenser'] = condenser
unit_dict['reboiler'] = reboiler

feed_flow_spec = Specify(flow=True, stream=feed, value=100)
feed_temp_spec = Specify(temperature=True, stream=feed, value=100)
feed_ic4_spec = Specify(fraction=True, stream=feed, comp_num=0, value=0.1)
feed_nc4_spec = Specify(fraction=True, stream=feed, comp_num=1, value=0.3)
feed_ic5_spec = Specify(fraction=True, stream=feed, comp_num=2, value=0.2)
feed_nc5_spec = Specify(fraction=True, stream=feed, comp_num=3, value=0.3)
feed_nc6_spec = Specify(fraction=True, stream=feed, comp_num=4, value=0.1)

top_product_flow_spec = Specify(flow=True, stream=top_product, value=40)

reflux_flow_spec = Specify(flow=True, stream=reflux, value=120)

unit_dict['feed_flow_spec'] = feed_flow_spec
unit_dict['feed_temp_spec'] = feed_temp_spec
unit_dict['feed_ic4_spec'] = feed_ic4_spec
unit_dict['feed_nc4_spec'] = feed_nc4_spec
unit_dict['feed_ic5_spec'] = feed_ic5_spec
unit_dict['feed_nc5_spec'] = feed_nc5_spec
unit_dict['feed_nc6_spec'] = feed_nc6_spec
unit_dict['top_product_flow_spec'] = top_product_flow_spec
unit_dict['reflux_flow_spec'] = reflux_flow_spec

# instantiate distillation column in E.g. 8-11 in Foust, et. al.
foust_8_11 = SimpleColumn(n_trays=15, feed_tray=7, 
                          feed_stream_liq=feed, 
                          reflux=reflux, 
                          vapor_reboil=vapor_reboil, 
                          condensate = condensate,
                          bottoms = bottoms,
                          press=45, 
                          tray_efficiency={5:0.8},
                          name='foust_8_11')

unit_dict[foust_8_11.name] = foust_8_11

n_eqns = 0
for u in unit_dict:
    n_eqns += unit_dict[u].num_eqns()
    
n_vars = 0
for u in unit_dict:
    n_vars += unit_dict[u].num_vars()
    
assert n_eqns == n_vars, 'Column is NOT OK'
print('Column is OK')

xvar = np.ones(n_vars, dtype=np.float64) * 100
map_var_to_unit1(xvar, unit_dict)
eqns = np.ones(n_vars, dtype=np.float64)
map_eqn_to_unit1(eqns, unit_dict)
#process_eqns(xvar);
x_solution = fsolve(process_eqns, xvar, args=(unit_dict, eqns))
print(np.sum(np.square(eqns)))
map_var_to_unit1(x_solution, unit_dict)

foust_profile = foust_8_11.profile()
print(foust_profile)

plt.figure()
plt.plot(foust_profile['T'], foust_profile['tray_num'], '-')
plt.xlabel('temperature')
plt.ylabel('tray number')
plt.grid(axis='both')

plt.figure()
plt.plot(foust_profile['x0'], foust_profile['tray_num'], '-')
plt.plot(foust_profile['x1'], foust_profile['tray_num'], '-')
plt.plot(foust_profile['x2'], foust_profile['tray_num'], '-')
plt.plot(foust_profile['x3'], foust_profile['tray_num'], '-')
plt.plot(foust_profile['x4'], foust_profile['tray_num'], '-')
plt.xlabel('fraction')
plt.ylabel('tray number')
plt.grid(axis='both')
plt.legend(['ic4','nc4','ic5','nc5','nc6'])
