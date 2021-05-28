# -*- coding: utf-8 -*-
"""
Makes a connection between two streams.
The flow rates of the two streams can be equal, or differ by a specified
amount (positive or negative). Can be used to model a leak, but the leak
is lost - it is not captured by another stream.
The temperatures of the two streams can be equal, or differ by a specified
amount (positive or negative). Can be used to model a heat leak.
The fraction of each component has to be the same for each stream.
"""

from unit import Unit
import numpy as np

class Connector(Unit):

    n_connectors = 0

    def __init__(self, stream_in, stream_out, flow_diff=0, temp_diff=0,
                 name=None):
        self.connector_num = Connector.n_connectors
        super().__init__(name, self.connector_num)
        Connector.n_connectors += 1
        self.stream_in = stream_in
        self.stream_out = stream_out
        self.n_vars = 0
        self.n_eqns = self.stream_in.n_comps + 2
        self.flow_diff = flow_diff
        self.temp_diff = temp_diff
        self.xvar = None
        self.eqns = np.zeros(self.n_eqns, dtype=np.float64)

    def __str__(self):
        s = ''
        s = s + 'Connector number: {}\n'.format(self.connector_num)
        s = s + 'Stream in: {}\n'.format(self.stream_in.name)
        s = s + 'Stream out: {}\n'.format(self.stream_out.name)
        s = s + 'Number of variables: {}\n'.format(self.n_vars)
        s = s + 'Number of equations: {}\n'.format(self.n_eqns)
        if self.eqns is None:
            s = s + 'Equations not set\n'
        else:
            s = s + 'Equations: {}\n'.format(self.eqns[:])
        return s

    def calculate(self):
        # equate flow: 1 equation
        self.eqns[0] = self.stream_in.xvar[0] + self.flow_diff - self.stream_out.xvar[0]
        # equate temperature: 1 equation
        self.eqns[1] = self.stream_in.xvar[1] + self.temp_diff - self.stream_out.xvar[1]
        # equate component fractions: n_comps equations
        for i_comp in range(self.stream_in.n_comps):
            self.eqns[2 + i_comp] = self.stream_in.xvar[2 + i_comp] - self.stream_out.xvar[2 + i_comp]
        return

    def update_flow_diff(self, flow_diff):
        self.flow_diff = flow_diff
        return

    def update_temp_diff(self, temp_diff):
        self.temp_diff = temp_diff
        return
