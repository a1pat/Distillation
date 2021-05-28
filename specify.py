# -*- coding: utf-8 -*-
"""
Specify a value for one of the following attributes of a Stream object:
    flowrate
    temperature
    fraction of a specified component
"""

from unit import Unit
import numpy as np

class Specify(Unit):
    
    n_specs = 0
    
    def __init__(self, name=None, flow=False, temperature=False, fraction=False, 
                 stream=None, comp_num=None, value=None):
        self.spec_num = Specify.n_specs
        super().__init__(name, self.spec_num)
        Specify.n_specs += 1
        assert flow + temperature + fraction == 1, 'Too many/few specifications for ' + self.name
            
        self.flow = flow
        self.temperature = temperature
        self.fraction = fraction
        self.stream = stream
        self.comp_num = comp_num
        self.value = value
        self.n_vars = 0
        self.n_eqns = 1
        self.xvar = None
        self.eqns = np.zeros(self.n_eqns, dtype=np.float64)
        

    def __str__(self):
        s = ''
        s = s + 'Specification name: {}\n'.format(self.name)
        s = s + 'Stream : {}\n'.format(self.stream.name)
        s = s + 'Number of variables: {}\n'.format(self.n_vars)
        s = s + 'Number of equations: {}\n'.format(self.n_eqns)
        if self.flow:
            s = s + 'Flow: {}\n'.format(self.value)
        elif self.temperature:
            s = s + 'Temperature: {}\n'.format(self.value)
        elif self.fraction:
            s = s + 'Fraction: component {}, value: {}\n'.format(self.comp_num, self.value)            
            
        if self.eqns is None:
            s = s + 'Equations not set\n'
        else:
            s = s + 'Equations: {}\n'.format(self.eqns[:])
        return s
    
    def calculate(self):
        if self.flow:
            self.eqns[0] = self.value -  self.stream.xvar[0]
        if self.temperature:
            self.eqns[0] = self.value -  self.stream.xvar[1]
        if self.fraction:
            self.eqns[0] = self.value -  self.stream.xvar[2 + self.comp_num]
        return
    
    def update(self, value):
        self.value = value
        return