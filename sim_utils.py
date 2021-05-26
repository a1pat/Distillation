# -*- coding: utf-8 -*-
"""
Utility functions used in the running of a simulation.
"""

def map_var_to_unit1(x, unit_dict):
    """
    Map simulation variable array to the variables in each Unit object
    in unit_dict.
    Parameters
    ----------
    x : array
        variable array used by the nonlinear equation solver.
    unit_dict : dict
        dictionary containing all Unit objects in the simulation.

    Returns
    -------
    None.

    """

    def map_var_to_unit2(x, unit_dict, idx):
        
        for u in unit_dict:
            n_vars = unit_dict[u].n_vars
            if n_vars > 0:
                unit_dict[u].xvar = x[idx:idx+n_vars]
                idx += n_vars
            map_var_to_unit2(x, unit_dict[u].unit_dict, idx)

    idx = 0
    map_var_to_unit2(x, unit_dict, idx)
    
    
def map_eqn_to_unit1(e, unit_dict):
    """
    Map equation array to the equations in each Unit object
    in unit_dict.
    Parameters
    ----------
    e : array
        equation array used by the nonlinear equation solver.
    unit_dict : dict
        dictionary containing all Unit objects in the simulation.

    Returns
    -------
    None.

    """

    def map_eqn_to_unit2(e, unit_dict, idx):
        for u in unit_dict:
            n_eqns = unit_dict[u].n_eqns
            if n_eqns > 0:
                unit_dict[u].eqns = e[idx:idx+n_eqns]
                idx += n_eqns
            map_eqn_to_unit2(e, unit_dict[u].unit_dict, idx)

    idx = 0
    map_eqn_to_unit2(e, unit_dict, idx)
    
    
def process_eqns(xvar):
    """
    Evaluates the equations of each Unit object.
    Parameters
    ----------
    xvar : array
        variable array for which to evaluate the equations.

    Returns
    -------
    array
        equations for each Unit object.

    """
    map_var_to_unit1(xvar, unit_dict)
    for u in unit_dict:
        unit_dict[u].calculate()
    return eqns.tolist()

