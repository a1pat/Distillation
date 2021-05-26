# -*- coding: utf-8 -*-
"""
Antoine constants for saturated vapor pressure.
"""

import numpy as np

# Antoine constants for saturate vapor pressure for 
# i-butane, n-butane, i-pentane, n-pentane, n-hexane
# form of the equation is
# p_sat (psia) = A - B / (C + T(F))
# above data from E.g. 8-11 in the textbook by Foust, et. al.

phy_props = {'Antoine_A': np.array((5.03458, 5.11679, 5.07617, 5.13871, 5.16426)),
             'Antoine_B': np.array((1589.04, 1702.62, 1836.0216, 1916.334, 2108.754)),
             'Antoine_C': np.array((400, 400, 387.575, 385.6, 371.859))}
