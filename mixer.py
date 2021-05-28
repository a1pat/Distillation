# -*- coding: utf-8 -*-
"""
A specified list of streams, each represented by a Stream object, enter
the Mixer object. A specified list of streams leave the Mixer object.
"""

from unit import Unit
import numpy as np

class Mixer(Unit):
    
    n_mixers = 0
    
    def __init__(self, streams_in, streams_out, name=None):
        self.mixer_num = Mixer.n_mixers
        super().__init__(name, self.mixer_num)
        Mixer.n_mixers += 1
        self.streams_in = streams_in
        self.streams_out = streams_out
        self.n_in = len(self.streams_in)
        self.n_out = len(self.streams_out)
        self.n_vars = 0
        self.n_eqns = (self.streams_in[0].n_comps + 1) * self.n_out + 1
        self.xvar = None
        self.eqns = np.zeros(self.n_eqns, dtype=np.float64)

    def __str__(self):
        s = 'Mixer name: {}\n'.format(self.name)
        s = s + 'Mixer number: {}\n'.format(self.mixer_num)
        s_in = list()
        for stream in self.streams_in:
            s_in.append(stream.name)
        s = s + 'Streams in: {}\n'.format(','.join(s_in))
        s_out = list()
        for stream in self.streams_out:
            s_out.append(stream.name)
        s = s + 'Streams out: {}\n'.format(', '.join(s_out))
        s = s + super().__str__()
        return s
    
    def calculate(self):
        # total mass balance: 1 equation
        total_in = 0
        for s in self.streams_in:
            total_in += s.xvar[0]
        total_out = 0
        for s in self.streams_out:
            total_out += s.xvar[0]
        self.eqns[0] = total_in - total_out
        
        # heat balance (simple: temp out is weighted average of temp in. n_out equations)
        t_avg_in = 0
        for s in self.streams_in:
            t_avg_in += s.xvar[0] * s.xvar[1]
        if total_in == 0:
            t_avg_in = self.streams_in[0].xvar[1]
        else:
            t_avg_in = t_avg_in / total_in
        eq_n = 0
        for s in self.streams_out:
            eq_n += 1
            self.eqns[eq_n] = t_avg_in - s.xvar[1]
        # component balances (n_out * n_comps equations)
        for i_comp in range(self.streams_in[0].n_comps):
            comp_in = 0
            for s in self.streams_in:
                comp_in += s.xvar[2 + i_comp] * s.xvar[0]
            if total_in == 0:
                comp_in = self.streams_in[0].xvar[2 + i_comp]
            else:
                comp_in = comp_in / total_in
            for s in self.streams_out:
                eq_n += 1
                self.eqns[eq_n] = comp_in - s.xvar[2 + i_comp]
        return