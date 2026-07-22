import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import matplotlib.pyplot as plt

from models.black_hole import BlackHole
from physics.ergospgere import Ergosphere

bh = BlackHole(
    mass = 1.0,
    spin = 0.9
)

ergo = Ergosphere(bh)

theta = np.linspace(
    0,
    np.pi,
    500
)

r = []

for t in theta:
    r.append(ergo.radius(t))

plt.plot(theta, r)

plt.xlabel("θ (radians)")
plt.ylabel("Ergosphere Radius")
plt.title("Outer Ergosphere")

plt.grid(True)

plt.show()