# -*- coding: utf-8 -*-
"""
Makes a connection between two streams.
The flow rate, temperaature and each component fraction of one Stream object
are specified to be equal to the corresponding attributes of the second Stream
object.
"""

from unit import Unit

class Connector(Unit):
    
    n_connectors = 0
    
    def __init__(self, stream_in, stream_out, name=None):
        self.connector_num = Connector.n_connectors
        super().__init__(name, self.connector_num)
        Connector.n_connectors += 1
        self.stream_in = stream_in
        self.stream_out = stream_out
        self.n_vars = 0
        self.n_eqns = self.stream_in.n_comps + 2

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
        self.eqns[0] = self.stream_in.xvar[0] - self.stream_out.xvar[0]
        # equate temperature: 1 equation
        self.eqns[1] = self.stream_in.xvar[1] - self.stream_out.xvar[1]
        # equate component fractions: n_comps equations
        for i_comp in range(self.stream_in.n_comps):
            self.eqns[2 + i_comp] = self.stream_in.xvar[2 + i_comp] - self.stream_out.xvar[2 + i_comp]
        return