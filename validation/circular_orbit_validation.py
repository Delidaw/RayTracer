import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))


import numpy as np
import matplotlib.pyplot as plt

from models.black_hole import BlackHole
from physics.initial_conditions import InitialConditions
from physics.orbit_simulator import OrbitSimulator

bh = BlackHole(mass = 1)

initial = InitialConditions(bh).circular_orbit(
    radius = 10
)

simulator = OrbitSimulator(bh)

trajectory = simulator.simulate(
    initial,
    step_size = 0.01,
    steps = 30000
)

r = trajectory[:, 1]

print("Expected radius :", 10)
print("Minimum radius  :", r.min())
print("Maximum radius  :", r.max())
print("Radius variation:", r.max() - r.min())

plt.plot(r)

plt.xlabel("Step")

plt.ylabel("Radius")

plt.title("Circular Orbit Radius Stability")

plt.grid(True)

plt.show()
