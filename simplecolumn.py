# -*- coding: utf-8 -*-
"""
Distillation column with a single saturated liquid feed stream.
Feed cannot be to the top or bottom tray.
Total condenser and total reboiler.
Same specified pressure on each tray.
"""

import numpy as np
import pandas as pd
from unit import Unit
from stream import Stream
from tray import Tray
from connector import Connector
from mixer import Mixer

class SimpleColumn(Unit):
    
    n_columns = 0
    
    def __init__(self, n_trays, feed_tray, feed_stream_liq, reflux, vapor_reboil, condensate,
                 bottoms, pressure, tray_efficiency=1.0, name=None):
        '''
        feed_tray must be an integer between 1 and n_trays-2 (feed cannot be to the top or bottom trays for now)
        the bottom tray is tray number zero
        the top tray is tray number n_trays-1
        
        the default efficiency is 1 for all trays.
        if tray_efficiency is a scalar, it is used for all trays.
        if tray_efficiency is a dict (tray:efficiency), it is used for the specified trays. the remaining are
        assigned an efficiency of 1.
        '''
        self.column_num = SimpleColumn.n_columns
        super().__init__(name, self.column_num)
        SimpleColumn.n_columns += 1
        
        assert n_trays > 0, '{}: Number of tray must be greater than zero (specified {})'.format(self.name, n_trays)
        self.n_trays = n_trays
        
        assert (feed_tray >= 1) and (feed_tray <= self.n_trays-2), \
            '{}: Feed tray number must be from 1 to {} inclusive (specified {}). No feed to the top or bottom trays for now' \
            .format(self.name, self.n_trays-2, feed_tray)
        self.feed_tray = feed_tray
        
        self.feed_stream_liq = feed_stream_liq
        self.reflux = reflux
        self.vapor_reboil = vapor_reboil
        self.condensate = condensate
        self.bottoms = bottoms
        self.pressure = pressure
        self.n_vars = 0
        self.n_eqns = 0
        self.xvar = None
        self.eqns = None
            
        
        # figure out number of streams to be created as part of this column
        # for each tray, there are two streams leaving (one liquid, one vapor)
        # one liquid feed stream (comes from outside the column)
        # one stream that is a combination of the liquid feed stream and the liquid from the tray above the feed tray
        
        # create the streams associated with the column
        # tray liquid and vapor streams
        self.tray_liq_stream = []
        for i_tray in range(self.n_trays):
            name = self.name+'Tray'+str(i_tray)+'Liquid'
#            self.tray_liq_stream.append(Stream(n_comps=N_COMPS, name=name))
            self.tray_liq_stream.append(Stream(n_comps=self.feed_stream_liq.n_comps, name=name))

        self.tray_vap_stream = []
        for i_tray in range(self.n_trays):
            name = self.name+'Tray'+str(i_tray)+'Vapor'
#            self.tray_vap_stream.append(Stream(n_comps=N_COMPS, name=name))
            self.tray_vap_stream.append(Stream(n_comps=self.feed_stream_liq.n_comps, name=name))

        # create the mixed stream consisting of the feed stream and the liquid from the tray above the feed tray
        name = self.name+'MixedLiquidFeed'
#        self.mixed_liq_feed = Stream(n_comps=N_COMPS, name=name)
        self.mixed_liq_feed = Stream(n_comps=self.feed_stream_liq.n_comps, name=name)
        self.unit_dict[name] = self.mixed_liq_feed
        
        # create the mixer needed to mix the liquid feed and the liquid from the tray above the feed tray
        name=self.name+'FeedMixer'
        self.feed_mixer = Mixer(streams_in=[self.feed_stream_liq, self.tray_liq_stream[feed_tray+1]], 
                                streams_out=[self.mixed_liq_feed],
                                name=name)
        self.unit_dict[name] = self.feed_mixer
        
        # create trays
        self.trays = []
        for i_tray in range(self.n_trays):
            name=self.name+'Tray'+str(i_tray)
            if i_tray == self.feed_tray:
                self.trays.append(Tray(liq_stream_in=self.mixed_liq_feed, 
                                       liq_stream_out=self.tray_liq_stream[i_tray],
                                       vap_stream_in=self.tray_vap_stream[i_tray-1], 
                                       vap_stream_out=self.tray_vap_stream[i_tray], 
                                       tray_efficiency=1, # will be updated later
                                       pressure=self.pressure, 
                                       name=name))
            elif i_tray == 0:
                self.trays.append(Tray(liq_stream_in=self.tray_liq_stream[i_tray+1], 
                                       liq_stream_out=self.tray_liq_stream[i_tray],
                                       vap_stream_in=self.vapor_reboil, 
                                       vap_stream_out=self.tray_vap_stream[i_tray], 
                                       tray_efficiency=1, # will be updated later
                                       pressure=self.pressure, 
                                       name=name))
            elif i_tray == self.n_trays-1:
                self.trays.append(Tray(liq_stream_in=self.reflux, 
                                       liq_stream_out=self.tray_liq_stream[i_tray],
                                       vap_stream_in=self.tray_vap_stream[i_tray-1], 
                                       vap_stream_out=self.tray_vap_stream[i_tray], 
                                       tray_efficiency=1, # will be updated later
                                       pressure=self.pressure, 
                                       name=name))
            else:
                self.trays.append(Tray(liq_stream_in=self.tray_liq_stream[i_tray+1], 
                                       liq_stream_out=self.tray_liq_stream[i_tray],
                                       vap_stream_in=self.tray_vap_stream[i_tray-1], 
                                       vap_stream_out=self.tray_vap_stream[i_tray], 
                                       tray_efficiency=1, # will be updated later
                                       pressure=self.pressure, 
                                       name=name))
                
        self.update_tray_efficiency(tray_efficiency)
                
        for s in self.tray_liq_stream:
            self.unit_dict[s.name] = s

        for s in self.tray_vap_stream:
            self.unit_dict[s.name] = s
        
        for s in self.trays:
            self.unit_dict[s.name] = s
        
        name = self.name+'CondensateConnector'
        self.condensate_connector = Connector(self.condensate, self.tray_vap_stream[n_trays-1], name=name)
        self.unit_dict[name] = self.condensate_connector
            
        name = self.name+'BottomsConnector'
        self.bottoms_connector = Connector(self.bottoms, self.tray_liq_stream[0], name=name)
        self.unit_dict[name] = self.bottoms_connector
            
    def __str__(self):
        s = 'SimpleColumn name: {}\n'.format(self.name)
        s = s + 'SimpleColumn number: {}\n'.format(self.column_num)
        s = s + 'Number of trays: {}\n'.format(self.n_trays)
        s = s + 'Feed tray: {}\n'.format(self.feed_tray)
        s = s + 'Pressure: {}\n'.format(self.pressure)
        s = s + 'Liquid feed stream: {}\n'.format(self.feed_stream_liq.name)
        s = s + 'Reflux stream: {}\n'.format(self.reflux.name)
        s = s + 'Vapor reboil stream: {}\n'.format(self.vapor_reboil.name)
        s = s + 'Tray efficiencies: {}\n'.format(self.tray_efficiency)
        s = s + super().__str__()
        return s
        
    def calculate(self):
        for u in self.unit_dict:
            self.unit_dict[u].calculate()
            
    def profile(self):
        '''
        return a pandas data frame containing the flow, temperature and composition profiles for each of the trays
        the row for each tray contains the following columns:
        0: tray number
        1: liquid flow from tray
        2: vapor flow from tray
        3: tray temperature
        4:4+n_comps: liquid fractions
        4+n_comps:4+2*n_comps: vapor fractions
        '''
        p = np.ones((self.n_trays, 2 * self.trays[0].liq_stream_out.n_vars), dtype=np.float64) * (-1)
        n_comps = self.trays[0].liq_stream_out.n_comps
        cols = ['tray_num','L','V','T']
        cols = cols + ['{}'.format(a+str(b)) for a,b in zip(n_comps*['x'], range(n_comps))]
        cols = cols + ['{}'.format(a+str(b)) for a,b in zip(n_comps*['y'], range(n_comps))]
        for i_tray in range(self.n_trays):
            p[i_tray, 0] = i_tray
            p[i_tray, 1] = self.trays[i_tray].liq_stream_out.xvar[0]
            p[i_tray, 2] = self.trays[i_tray].vap_stream_out.xvar[0]
            p[i_tray, 3] = self.trays[i_tray].liq_stream_out.xvar[1]
            p[i_tray, 4:4+n_comps] = self.trays[i_tray].liq_stream_out.xvar[2:]
            p[i_tray, 4+n_comps:4+2*n_comps] = self.trays[i_tray].vap_stream_out.xvar[2:]
        return pd.DataFrame(data=p, columns=cols)
    
    def update_press(self, pressure):
        self.pressure = pressure
        for tray in self.trays:
            tray.update_pressure(self.pressure)
        return
    
    def update_tray_efficiency(self, tray_efficiency):
        # make list of tray efficiencies
        if isinstance(tray_efficiency, dict):
            self.tray_efficiency = [1.0] * self.n_trays
            for t, eff in tray_efficiency.items():
                self.tray_efficiency[t] = eff
        else: # assume it is a scalar
            self.tray_efficiency = [tray_efficiency] * self.n_trays
            
        for i, tray in enumerate(self.trays):
            tray.update_tray_efficiency(self.tray_efficiency[i])
        return
        