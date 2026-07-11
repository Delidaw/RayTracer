import numpy as np
import matplotlib.pyplot as plt

from models.black_hole import BlackHole
from physics.initial_conditions import InitialConditions
from physics.geodesics import GeodesicEquation
from physics.integrator import RK4Integrator
from physics.orbit_simulator import OrbitSimulator

bh = BlackHole(mass = 1)

initial = InitialConditions(bh).escape_trajectory(
    radius = 20,
    radial_velocity = 0.15,
    angular_velocity = 0.15
)

#equation = GeodesicEquation(bh)

#integrator = RK4Integrator(bh)

simulator = OrbitSimulator(bh)

trajectory = simulator.simulate(
    initial, 
    step_size = 0.01,
    steps = 20000
)
"""
print("Initial radius :", trajectory[0, 1])
print("Final radius   :", trajectory[-1, 1])

print("Maximum radius :", trajectory[:, 1].max())
print("Minimum radius :", trajectory[:, 1].min())
"""

r = trajectory[:, 1]
phi = trajectory[:, 3]

x = r * np.cos(phi)
y = r * np.sin(phi)

plt.figure(figsize = (7, 7))
plt.plot(x, y, label = "Escape trajectory")

plt.scatter(0, 0, s = 150, color = "black", label = "Black Hole")

plt.gca().set_aspect("equal")

plt.xlabel("x")
plt.ylabel("y")

plt.legend()

plt.grid(True)

plt.show()