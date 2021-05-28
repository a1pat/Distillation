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
                #print(u, idx, idx+n_vars-1)
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
        for u in unit_dict:
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
    for u in unit_dict:
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
