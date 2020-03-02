# Code to generate the coordinate points for Horns Rev 1

# Import packages
import numpy as np
import matplotlib.pyplot as plt
import floris.tools.optimization as optimization
import floris
import floris.tools as wfct
import time

# Initialize the FLORIS interface fi
fi = wfct.floris_utilities.FlorisInterface("hornsrev.json")        
# Define farm geometry
n_col = 10
n_row = 8

# Rotor diameter- Used for turbine spacing
D = 80

# Skew angles for grid (Degrees)
x_skew = 0
y_skew = 7.2

# Calculate farm geometery
x_space = 7*D
y_space = 7*D

# Initialize farm grid
Farm1 = optimization.lay_opt(n_row,n_col,x_skew,y_skew,D,x_space,y_space)
Farm1.generate_grid()

Farm1.write_out('hornsrev')