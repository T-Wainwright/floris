# Copyright 2019 NREL

# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from tests.sample_inputs import SampleInputs
import json

# import warnings
# warnings.simplefilter('ignore', RuntimeWarning)


def optimize_yaw(fi, minimum_yaw_angle=0.0, maximum_yaw_angle=25.0):
    """
    Find optimum setting of turbine yaw angles for power production
    given fixed atmospheric conditins (wind speed, direction, etc.)

    Args:
        fi (:py:class:`floris.tools.floris_utilities.FlorisInterface`):
            Interface from FLORIS to the wfc tools
        minimum_yaw_angle (float, optional): minimum constraint on yaw.
            Defaults to 0.0.
        maximum_yaw_angle (float, optional): maximum constraint on yaw.
            Defaults to 25.0.

    Returns:
        opt_yaw_angles (np.array): optimal yaw angles of each turbine.
    """
    # initialize floris without the full flow domain; only points assigned at the turbine
    fi.floris.farm.flow_field.reinitialize_flow_field()

    # set initial conditions
    x0 = []
    bnds = []

    turbines = fi.floris.farm.turbine_map.turbines
    x0 = [turbine.yaw_angle for turbine in turbines]
    bnds = [(minimum_yaw_angle, maximum_yaw_angle) for turbine in turbines]

    print('=====================================================')
    print('Optimizing wake redirection control...')
    print('Number of parameters to optimize = ', len(x0))
    print('=====================================================')

    residual_plant = minimize(fi.get_power_for_yaw_angle_opt,
                              x0,
                              method='SLSQP',
                              bounds=bnds,
                              options={'eps': np.radians(5.0)})

    if np.sum(residual_plant.x) == 0:
        print('No change in controls suggested for this inflow condition...')

    # %%
    opt_yaw_angles = residual_plant.x

    return opt_yaw_angles

class lay_opt:

    def __init__(self, n_row, n_col, x_skew, y_skew, D, x_space, y_space):
        # Initialise farm variables
        self.n_row = n_row
        self.n_col = n_col
        self.x_skew = np.radians(x_skew)
        self.y_skew = np.radians(y_skew)
        self.D = D
        self.x_space = x_space
        self.y_space = y_space
        self.n_turb = n_row*n_col
        self.farm = []

        # Create array to store turbine positions
        self.positions = np.zeros((self.n_turb,2))
        # Create transformation matrix
        self.T=[[np.cos(self.x_skew), -np.sin(self.y_skew)], [np.sin(self.x_skew), np.cos(self.y_skew)]]
        

    def generate_grid(self):
        # Generate initial grid
        X, Y = np.mgrid[0:self.n_col, 0:self.n_row]
        X = X * self.x_space
        Y = Y * self.y_space
        positions = np.vstack([X.ravel(), Y.ravel()])

        # Apply skew
        positions2 = np.transpose(np.matmul(self.T,positions))

        # Position farm to fully within the domain, and store
        self.positions[:,0] = positions2[:,0] - np.min(positions2[:,0])
        self.positions[:,1] = positions2[:,1] - np.min(positions2[:,1])

        return()

    def plot_farm(self):
        plt.plot(self.positions[:,0],self.positions[:,1],'.')
        plt.show()

    def write_out(self,ftag):
        with open(ftag, 'w') as f:
            for point in self.positions:
                f.write("%f, %f\n" % (point[0], point[1]))
    
    def modify(self,x_row_shift,x_col_shift,y_row_shift,y_col_shift):
        ii = 0

        for j in range(self.n_col):
            for i in range(self.n_row):
                # Create perturbation vector
                delta = (x_col_shift[j]+x_row_shift[i],y_col_shift[j]+y_row_shift[i])
                # Apply perturbation vector
                self.positions[ii,:] = self.positions[ii,:] + np.matmul(self.T,delta)
                ii=ii+1

    def write2json(self,Input_file,name,description):
        farm1 = SampleInputs()
        
        farm1.farm["properties"]["layout_x"]=self.positions[:,0].tolist()
        farm1.farm["properties"]["layout_y"]=self.positions[:,1].tolist()

        farm2 = {"type" : "floris_input", "name" : name, "description" : description, "farm" : farm1.farm,"turbine" : farm1.turbine, "wake" : farm1.wake}

        with open(Input_file, 'w') as f:
            json.dump(farm2, f,sort_keys=True, indent=2, separators=(',', ': '))

