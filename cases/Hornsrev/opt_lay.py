import floris.tools as wfct
import scipy.optimize as opt
import numpy as np

def costfunc(X):
    # Cost function for WFLO problem using floris

    # Unpack vector
    x_col_shift = X[0:n_col]
    y_col_shift = X[n_col:]
    # Row shift directions
    y_row_shift = (0,0,0,0) # leave as 0 for reduced dimensionality for now
    x_row_shift = (0,0,0,0)

    wind_dir = (0,90,180,360) # Edit number of wind directions to be examined here

    # Reset field- need to do this each iteration to prevent runaway
    Farm.generate_grid()

    # Apply perturbations
    Farm.modify(x_row_shift,x_col_shift,y_row_shift,y_col_shift)

    fi.reinitialize_flow_field(layout_array=(Farm.positions[:,0].tolist(), Farm.positions[:,1].tolist()))

    # Reset Power

    POWER = 0
    
    # Allows for bulky multiple wind directions- comment out if not needed
    for wind in wind_dir:
        fi.reinitialize_flow_field(wind_direction=wind)
        fi.calculate_wake()
        POWER = POWER + fi.get_farm_power()

    return -POWER

""" Generate initial farm geometry """
       
# Define farm geometry
n_col = 5       # Number of rows
n_row = 4       # Number of columns
D = 80          # Turbine Diameter (Needed for spacing)
x_skew = 0      # X direction skew (angle to horizontal)
y_skew = 7.2    # Y direction skew (angle to vertical)

# Calculate farm geometery
x_space = 7*D   # Turbine spacing in the x direction
y_space = 7*D   # Turbine spacing in the y direction

# Initialize farm grid
Farm = wfct.optimization.lay_opt(n_row,n_col,x_skew,y_skew,D,x_space,y_space)
Farm.generate_grid()
fi = wfct.floris_utilities.FlorisInterface("hornsrev.json") # Read input file- leave turbine and machinery performance in here, layout is handled in code
fi.reinitialize_flow_field(layout_array=(Farm.positions[:,0].tolist(), Farm.positions[:,1].tolist())) # Set initial grid layout

""" Generate optimization problem"""

# Column shift directions
x_col_shift = (0,2*D,0,0,0)
y_col_shift = (0,0,0,0,0)

# Assemble linear design vector
x0 = (x_col_shift + y_col_shift)
power = costfunc(x0)
Farm.plot_farm()    # Plot initial layout

# Define bounds- currently just set to adjust the row spacing

x_bnds = []
y_bnds = []
bnds = []
x_bnds = [(-2*D, 2*D) for i in range(n_col)]
y_bnds = [(-2*D, 2*D) for i in range(n_col)]
bnds = x_bnds + y_bnds

print(bnds)

""" Optimization Unit- local and global options available here, currently just using a bounded problem"""

i_max = 100     # Maximum number of optimization iterations
res = opt.minimize(costfunc,x0,bounds=bnds,options={'gtol': 1e-8, 'disp': True, 'maxiter' : i_max},) # Default L-BFGS-B
# res = opt.dual_annealing(costfunc,bounds=bnds,maxiter=i_max) # Simulated annealing

# Display results

print('Optimization Complete')
power = costfunc(res.x)
print(res.x)
print(power)
Farm.plot_farm()