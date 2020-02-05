# Code to generate the coordinate points for Horns Rev 1

# Import packages
import numpy as np
import matplotlib.pyplot as plt
import floris.tools.optimization as optimization
import floris
        
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

Farm1 = optimization.lay_opt(n_row,n_col,x_skew,y_skew,D,x_space,y_space)

Farm1.generate_grid()

# Farm1.plot_farm()

Farm1.write_out('hornsrev.pts')

# Define perturbation vectors

# Column shift directions
y_col_shift = (0,0,0,D,0,0,2*D,0,0,0)
x_col_shift = (0,0,0,D,0,-D,0,0,0,0)

# Row shift directions
y_row_shift = (0,0,D,0,3*D,0,0,0)
x_row_shift = (0,-2*D,D,0,0,0,0,0)

Farm1.modify(x_row_shift,x_col_shift,y_row_shift,y_col_shift)

# Farm1.plot_farm()

# output points to json file
Farm1.write2json('TEST.json', 'test','a simple test json')

