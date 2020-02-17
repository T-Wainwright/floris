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

# Define perturbation vectors

# Column shift directions
y_col_shift = (0,2*D,0,0,0,0,0,0,0,0)
x_col_shift = (0,0,0,0,0,5*D,0,0,0,0)

# Row shift directions
y_row_shift = (0,0,0,0,0,0,0,0)
x_row_shift = (0,0,0,0,0,0,0,0)

# Apply perturbations
Farm1.modify(x_row_shift,x_col_shift,y_row_shift,y_col_shift)
fi.reinitialize_flow_field(layout_array=(Farm1.positions[:,0].tolist(), Farm1.positions[:,1].tolist()))

print(y_row_shift)
Farm1.plot_farm()