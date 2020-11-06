import numpy as np
from Grid.GridProcessing import Grid
from Shapes.ShapesFunctions import *

# Specify the  file that includes dynamic systems
from dynamics.DubinsCar4D2 import *
import math

""" USER INTERFACES
- Define grid

- Generate initial values for grid using shape functions

- Time length for computations

- Run
"""

g = Grid(
    np.array([-3.0, -1.0, -1.0, -math.pi]),
    np.array([3.0, 4.0, 5.0, math.pi]),
    4,
    np.array([40, 40, 30, 30]),
    # np.array([60, 60, 50, 50]),
    # np.array([30, 30, 20, 20]),
    [3],
)

# Define my object
my_car = DubinsCar4D2()

# Use the grid to initialize initial value function
# Initial_value_f = CylinderShape(g, [3, 4], np.array([0.0, 1.0, 0.0, 0.0]), 0.70)
Initial_value_f = np.minimum.reduce([CylinderShape(g, [3, 4], np.array([0.0, -0.3 + 1.0, 0.0, 0.0]), 0.70),
                             CylinderShape(g, [3, 4], np.array([0.00, -0.15 + 1.0, 0.0, 0.0]), 0.70),
                             CylinderShape(g, [3, 4], np.array([0.0, 1.0, 0.0, 0.0]), 0.70),
                             CylinderShape(g, [3, 4], np.array([0.00, 1.15, 0.0, 0.0]), 0.70),
                             CylinderShape(g, [3, 4], np.array([0.0, 1.3, 0.0, 0.0]), 0.70)])

# Look-back lenght and time step
lookback_length = 1.8
t_step = 0.05

small_number = 1e-5
tau = np.arange(start=0, stop=lookback_length + small_number, step=t_step)
print("Welcome to optimized_dp \n")
print("")

"""
Assign one of the following strings to `compMethod` to specify the characteristics of computation
"none" -> compute Backward Reachable Set
"minVWithV0" -> compute Backward Reachable Tube
"maxVWithVInit" -> compute max V over time
"minVWithVInit" compute min V over time
"""
compMethod = "minVWithV0"
my_object = my_car
my_shape = Initial_value_f
