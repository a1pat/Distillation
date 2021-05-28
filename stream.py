# -*- coding: utf-8 -*-
"""
Stream object contains flow rate, temperature and fraction of each component.
"""

from unit import Unit
import numpy as np

class Stream(Unit):
    
    n_streams = 0
    
    def __init__(self, n_comps=1, name=None):
        self.stream_num = Stream.n_streams
        super().__init__(name, self.stream_num)
        Stream.n_streams += 1
        # the stream member x_var will be as follows:
        # [0] flow rate
        # [1] temperature
        # [2:] fraction of each component. if flow is in mass units, these are mass fractions
        self.n_comps = n_comps
        self.n_vars = 2 + n_comps
        self.n_eqns = 0
        self.xvar = np.zeros(self.n_vars, dtype=np.float64)
        self.eqns = None
        
    def __str__(self):
        s = 'Stream name: {}\n'.format(self.name)
        s = s + 'Stream number: {}\n'.format(self.stream_num)
        s = s + 'Number of variables: {}\n'.format(self.n_vars)
        s = s + 'Number of equations: {}\n'.format(self.n_eqns)
        if self.xvar is None:
            s = s + 'Variables not set\n'
        else:
            s = s + 'Flow rate: {}\n'.format(self.xvar[0])
            s = s + 'Temperature: {}\n'.format(self.xvar[1])
            s = s + 'Fractions: {}\n'.format(self.xvar[2:])
        return s
    
    def calculate(self):
        pass