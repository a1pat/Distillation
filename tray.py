# -*- coding: utf-8 -*-
"""
Tray of a distillation column.
Tray can have efficiency different than 1.
Equimolal overflow assumed.
Tray operates at specified pressure.
"""

import numpy as np
from unit import Unit
from phy_props import phy_props


class Tray(Unit):
    
    global Antoine_A
    
    n_trays = 0
    
    def __init__(self, liq_stream_in, liq_stream_out, vap_stream_in, vap_stream_out, pressure, tray_efficiency=1, name=None):
        self.tray_num = Tray.n_trays
        super().__init__(name, self.tray_num)
        Tray.n_trays += 1
        self.liq_stream_in = liq_stream_in
        self.liq_stream_out = liq_stream_out
        self.vap_stream_in = vap_stream_in
        self.vap_stream_out = vap_stream_out
        self.pressure = pressure
        self.n_vars = 0
        self.n_eqns = 2 * self.liq_stream_in.n_comps + 4
        self.tray_efficiency = tray_efficiency
        self.eqns = np.zeros(self.n_eqns, dtype=np.float64)
        

    def __str__(self):
        s = ''
        s = s + 'Tray name: {}\n'.format(self.name)
        s = s + 'Tray number: {}\n'.format(self.tray_num)
        s = s + 'Liquid stream in: {}\n'.format(self.liq_stream_in.name)
        s = s + 'Liquid stream out: {}\n'.format(self.liq_stream_out.name)
        s = s + 'Vapor stream in: {}\n'.format(self.vap_stream_in.name)
        s = s + 'Vapor stream out: {}\n'.format(self.vap_stream_out.name)
        s = s + 'Pressure: {}\n'.format(self.pressure)
        s = s + 'Number of variables: {}\n'.format(self.n_vars)
        s = s + 'Number of equations: {}\n'.format(self.n_eqns)
        s = s + 'Tray efficiency: {}\n'.format(self.tray_efficiency)
        if self.eqns is None:
            s = s + 'Equations not set\n'
        else:
            s = s + 'Equations: {}\n'.format(self.eqns[:])
        return s
    
    def calculate(self):
        
        global Antoine_A
        global Antoine_B
        global Antoine_C
        
        # total mass balance: 1 equation
        self.eqns[0] = self.liq_stream_in.xvar[0] + self.vap_stream_in.xvar[0] - \
            self.liq_stream_out.xvar[0] - self.vap_stream_out.xvar[0]
        # heat balance (simple: equimolal overflow. 1 equation)
        self.eqns[1] = self.liq_stream_in.xvar[0] - self.liq_stream_out.xvar[0]
        # heat balance (simple: liquid and vapor leaving tray have the same temperatures. 1 equation)
        self.eqns[2] = self.vap_stream_out.xvar[1] - self.liq_stream_out.xvar[1]
        # fractions sum to one (2 equations)
        sum_x = -1
        sum_y = -1
        for i_comp in range(self.liq_stream_in.n_comps):
            sum_x += self.liq_stream_out.xvar[2+i_comp]
            sum_y += self.vap_stream_out.xvar[2+i_comp]
        self.eqns[3] = sum_x
        self.eqns[4] = sum_y
        # component balances (n_comps equations)
        for i_comp in range(self.liq_stream_in.n_comps-1):
            self.eqns[5+i_comp] = self.liq_stream_in.xvar[0] * self.liq_stream_in.xvar[2+i_comp] + \
                self.vap_stream_in.xvar[0] * self.vap_stream_in.xvar[2+i_comp] - \
                self.liq_stream_out.xvar[0] * self.liq_stream_out.xvar[2+i_comp] - \
                self.vap_stream_out.xvar[0] * self.vap_stream_out.xvar[2+i_comp]
        # vapor-liquid equilibrium (n_comps equations)
        for i_comp in range(self.liq_stream_in.n_comps):
#            K_eq = np.power(10, Antoine_A[i_comp] - Antoine_B[i_comp] / (Antoine_C[i_comp] + self.liq_stream_out.xvar[1])) / self.press
            K_eq = np.power(10, phy_props['Antoine_A'][i_comp] - phy_props['Antoine_B'][i_comp] / (phy_props['Antoine_C'][i_comp] + self.liq_stream_out.xvar[1])) / self.pressure
            K_eq = self.tray_efficiency * K_eq + (1 - self.tray_efficiency)
            self.eqns[4+self.liq_stream_in.n_comps+i_comp] = self.vap_stream_out.xvar[2+i_comp] - \
                K_eq * self.liq_stream_out.xvar[2+i_comp]
        return
    
    def update_pressure(self, pressure):
        self.pressure = pressure
        return
    
    def update_tray_efficiency(self, tray_efficiency):
        self.tray_efficiency = tray_efficiency
        return