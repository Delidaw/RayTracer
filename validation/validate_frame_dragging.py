import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import matplotlib.pyplot as plt

from models.black_hole import BlackHole

from physics.kerr_metric import KerrMetric
from physics.frame_dragging import FrameDragging


bh = BlackHole(
    mass=1,
    spin=0.9
)

metric = KerrMetric(bh)

drag = FrameDragging(metric)

r = np.linspace(2.1,40,500)

omega = []

for radius in r:

    omega.append(
        drag.omega(
            radius,
            np.pi/2
        )
    )

plt.plot(r, omega)

plt.xlabel("Radius")

plt.ylabel("Frame Dragging Ω")

plt.title("Kerr Frame Dragging")

plt.grid()

plt.show()