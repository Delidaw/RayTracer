#postponed after effective potential

import numpy as np
import matplotlib.pyplot as plt

from models.black_hole import BlackHole
from physics.initial_conditions import InitialConditions
from physics.orbit_simulator import OrbitSimulator

bh = BlackHole(mass = 1)

initial = InitialConditions(bh).elliptical_orbit(
    semi_major_axis = 20,
    eccentricity = 0.4
)

simulator = OrbitSimulator(bh)

trajectory = simulator.simulate(
    initial,
    step_size = 0.01,
    steps = 50000
)

r = trajectory[:, 1]
phi = trajectory[:, 3]

x = r * np.cos(phi)
y = r * np.sin(phi)

plt.figure(figsize=(8, 8))

plt.plot(x, y, linewidth = 2, label = "Elliptical Orbit")

#BlackHole
plt.scatter(0, 0, s = 150, color = "black")

#Event Horizon
R_s = bh.schwarzschild_radius

plt.gca().add_patch(
    plt.Circle(
        (0, 0),
        R_s, color = "black",
        alpha = 0.3
    )
)

#Start and end
plt.scatter(x[0], y[0], color = "green", s = 60, label = "Start")
plt.scatter(x[-1], y[-1], color = "red", s = 60, label = "End")

plt.gca().set_aspect("equal")

plt.xlabel("x")
plt.ylabel("y")
plt.title("Elliptical Orbit")

plt.grid(True)

plt.legend()

plt.show()