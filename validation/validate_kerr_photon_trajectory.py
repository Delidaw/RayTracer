import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import matplotlib.pyplot as plt

from models.black_hole import BlackHole
from physics.kerr_metric import KerrMetric
from physics.kerr_derivatives import KerrDerivatives
from physics.orbit_simulator import OrbitSimulator
from models.observer import Observer
from physics.kerr_ray_generator import KerrRayGenerator

bh = BlackHole(
    mass = 1.0,
    spin = 0.9
)

metric = KerrMetric(bh)

derivatives = KerrDerivatives(metric)

simulator = OrbitSimulator(
    metric,
    derivatives
)

observer = Observer(radius = 20.0)

generator = KerrRayGenerator(metric)

state = generator.generate(
    observer,
    np.array([0,0,1])
)

result = simulator.simulate(
    state,
    step_size = 0.01,
    steps = 50000
)

trajectory = result["trajectory"]

r = trajectory[:, 1]
phi = trajectory[:, 3]

x = r * np.cos(phi)
y = r * np.sin(phi)

plt.figure(figsize = (6,6))
plt.plot(x, y)

plt.scatter(0, 0, color = "black", s = 150)

plt.axis("equal")
plt.grid(True)

plt.show()