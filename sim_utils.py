# -*- coding: utf-8 -*-
"""
Utility functions used in the running of a simulation.
"""

import numpy as np

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
        
        for u in sorted(unit_dict.keys()):
            n_vars = unit_dict[u].n_vars
            if n_vars > 0:
                #print(type(x))
                unit_dict[u].xvar = x[idx:idx+n_vars]
                idx += n_vars
            idx = map_var_to_unit2(x, unit_dict[u].unit_dict, idx)
        return idx

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
        for u in sorted(unit_dict.keys()):
            n_eqns = unit_dict[u].n_eqns
            if n_eqns > 0:
                unit_dict[u].eqns = e[idx:idx+n_eqns]
#                e[idx:idx+n_eqns] = unit_dict[u].eqns
                #print(u, idx, idx+n_eqns-1)
                idx += n_eqns
            idx = map_eqn_to_unit2(e, unit_dict[u].unit_dict, idx)
        return idx

    idx = 0
    map_eqn_to_unit2(e, unit_dict, idx)
    
    
def process_eqns(xvar, unit_dict, eqns):
    """
    Evaluates the equations of each Unit object.
    Parameters
    ----------
    xvar : array
        variable array for which to evaluate the equations.
    unit_dict : dict
        dictionary containing all the Unit objects in the model.
    eqns : array
        equations for all the Unit objects in the model.

    Returns
    -------
    array
        evaluated equations for all the Unit objects in the model.

    """
    map_var_to_unit1(xvar, unit_dict)
    for u in sorted(unit_dict.keys()):
        unit_dict[u].calculate()
    return eqns.tolist()


def get_info(unit_dict):
    """
    Print model info.
    Parameters
    ----------
    unit_dict : dict
        dictionary containing all Unit objects in the simulation.

    Returns
    -------
    info : str
        information about the unit_dict

    """

    def get_info2(unit_dict, info):
        info = info + 'unit_dict contains {}'.format(list(unit_dict.keys()))
        for u in sorted(unit_dict.keys()):
            info = info + '\n' + str(unit_dict[u])
            if not unit_dict[u].unit_dict:
                info = info + u + ' has NO unit_dict \n'
            else:
                info = info + u + ' has a unit_dict with ' + str(len(unit_dict[u].unit_dict.keys())) + ' items\n'
                info = info + 'entering recursion\n'
                info = get_info2(unit_dict[u].unit_dict, info)
                info = info + 'exited recursion\n'
        return info

    info = get_info2(unit_dict, '')        
    return info


def get_num_vars(unit_dict):
    """
    calculate the total number of variables for all the units in unit_dict.

    Parameters
    ----------
    unit_dict : dict
        dictionary containing all the Unit objects in the simulation.

    Returns
    -------
    nvars : integer
        total number of variables.

    """
    nvars = 0
    for u in sorted(unit_dict.keys()):
        nvars += unit_dict[u].num_vars()
    return nvars


def get_num_eqns(unit_dict):
    """
    calculate the total number of equations for all the units in unit_dict.

    Parameters
    ----------
    unit_dict : dict
        dictionary containing all the Unit objects in the simulation.

    Returns
    -------
    neqns : integer
        total number of equations.

    """
    neqns = 0
    for u in sorted(unit_dict.keys()):
        neqns += unit_dict[u].num_eqns()
    return neqns


def get_unit_vars(unit_dict):
    """
    Get variable array of all the variables in each Unit object
    in unit_dict.
    Parameters
    ----------
    unit_dict : dict
        dictionary containing all Unit objects in the simulation.

    Returns
    -------
    x : array
        variable array used by the nonlinear equation solver.

    """

    def get_unit_vars_inner(x, unit_dict, idx):
        
        for u in sorted(unit_dict.keys()):
            n_vars = unit_dict[u].n_vars
            if n_vars > 0:
                #print(type(x))
                for i in range(n_vars):
                    x[idx+i] = unit_dict[u].xvar[i]
                idx += n_vars
            x, idx = get_unit_vars_inner(x, unit_dict[u].unit_dict, idx)
        return x, idx

    x = np.zeros(get_num_vars(unit_dict), dtype=np.float64)
    idx = 0
    x, idx = get_unit_vars_inner(x, unit_dict, idx)
    return x
    
    
