import numpy as np
from grid.grid_processing import Grid
from shapes.shape_functions import *
from dynamics.dubin_car_4d import DubinsCar4D
import math

""" USER INTERFACES
- Define grid

- Generate initial values for grid using shape functions

- Time length for computations

- Run
"""

g = Grid(
    np.array([-3.0, -1.0, 0.0, -math.pi]),
    np.array([3.0, 4.0, 1.0, math.pi]),
    4,
    np.array([60, 60, 30, 36]),
    [3],
)

# Define my object
my_car = DubinsCar4D()

# Use the grid to initialize initial value function
Initial_value_f = Rectangle6D(g)

# Look-back length and time step
lookback_length = 2.0
t_step = 0.05

tau = np.arange(start = 0, stop = lookback_length + t_step, step = t_step)
print("Welcome to optimized_dp \n")

# Use the following variable to specify the characteristics of computation
compMethod = "minVWithVInit"
my_object  = my_car
my_shape = Initial_value_f """

g = Grid(np.array([-5.0, -5.0, -1.0, -math.pi]), np.array([5.0, 5.0, 1.0, math.pi]), 4, np.array([40, 40, 50, 50]), [3])

# Define my object
my_car = DubinsCar4D()

# Use the grid to initialize initial value function
Initial_value_f = CylinderShape(g, [3,4], np.zeros(4), 1)

# Look-back lenght and time step
lookback_length = 2.0
t_step = 0.05

small_number = 1e-5
tau = np.arange(start = 0, stop = lookback_length + small_number, step = t_step)
print("Welcome to optimized_dp \n")

'''
Assign one of the following strings to `compMethod` to specify the characteristics of computation
"none" -> compute Backward Reachable Set
"minVwithV0" -> compute Backward Reachable Tube
"maxVwithVInit" -> compute max V over time
"minVwithVInit" compute min V over time
'''
compMethod = "none"
my_object  = my_car
my_shape = Initial_value_f


