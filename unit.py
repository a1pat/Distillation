# -*- coding: utf-8 -*-
"""
Parent class for classes for processing equipment and material streams.
"""

class Unit():
    def __init__(self, name, num):
        self.xvar = None
        self.eqns = None
        self.unit_dict = dict()
        if name is None:
            self.name = type(self).__name__ + str(num)
        else:
            self.name = name
        
    def num_eqns(self):
        num = self.n_eqns
        for u in self.unit_dict:
            num += self.unit_dict[u].num_eqns()
        return num        

    def num_vars(self):
        num = self.n_vars
        for u in self.unit_dict:
            num += self.unit_dict[u].num_vars()
        return num        