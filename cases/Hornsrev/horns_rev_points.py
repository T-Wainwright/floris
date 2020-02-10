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
y_col_shift = (0,0,0,D,0,0,2*D,0,0,0)
x_col_shift = (0,0,0,D,0,-D,0,0,0,0)

# Row shift directions
y_row_shift = (0,0,D,0,3*D,0,0,0)
x_row_shift = (0,-2*D,D,0,0,0,0,0)

# Apply perturbations
Farm1.modify(x_row_shift,x_col_shift,y_row_shift,y_col_shift)
fi.reinitialize_flow_field(layout_array=(Farm1.positions[:,0].tolist(), Farm1.positions[:,1].tolist()))

# Change the wake model
fi.floris.farm.set_wake_model('curl')

# wd = 6

# fi.reinitialize_flow_field(wind_direction=wd)
# # Calculate wake and time
# start = time.time()
# fi.calculate_wake()
# finish = time.time()
# print('Time to calculate flow field', finish - start)

# # Initialize the horizontal cut
# hor_plane = wfct.cut_plane.HorPlane(
#     fi.get_flow_data(),
#     fi.floris.farm.turbines[0].hub_height
# )

# # Plot and show
# fig, ax = plt.subplots()
# wfct.visualization.visualize_cut_plane(hor_plane, ax=ax)
# plt.show()

# turb_powers = fi.get_turbine_power()
# farm_power = fi.get_farm_power()
# total = 0

# for power in turb_powers:
#     total = total + power
#     print(total)

# # print(farm_power)
# fpower = []
# wind = []

# for wd in range(0,360,1):
#     print(wd)
#     fi.reinitialize_flow_field(wind_direction=wd)
#     fi.calculate_wake()
#     fpower.append(fi.get_farm_power())
#     wind.append(wd)

# # plt.plot(wind,fpower)
wd = 270
fi.reinitialize_flow_field(wind_direction=wd)

fi.calculate_wake()
power_normal = fi.get_farm_power()

print(power_normal)

min_yaw = -25
max_yaw = 25

yaw_angles = optimization.optimize_yaw(fi,min_yaw,max_yaw)

fi.calculate_wake(yaw_angles=yaw_angles)
power_opt = fi.get_farm_power()
print(power_opt)

# Initialize the horizontal cut
hor_plane = wfct.cut_plane.HorPlane(
    fi.get_flow_data(),
    fi.floris.farm.turbines[0].hub_height
)

print(yaw_angles)

# Plot and show
fig, ax = plt.subplots()
wfct.visualization.visualize_cut_plane(hor_plane, ax=ax)
plt.show()