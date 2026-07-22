import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import matplotlib.pyplot as plt

from models.black_hole import BlackHole
from models.observer import Observer

from physics.kerr_metric import KerrMetric
from physics.kerr_ray_generator import KerrRayGenerator
from physics.kerr_derivatives import KerrDerivatives
from physics.orbit_simulator import OrbitSimulator
from models.camera import Camera
from rendering.kerr_ray_tracer import KerrRayTracer

bh = BlackHole(
    mass=1.0,
    spin=0.9
)

metric = KerrMetric(bh)

observer = Observer(
    radius=20.0
)

generator = KerrRayGenerator(metric)

directions = [

    np.array([0,0,1]),

    np.array([0.2,0,1]),

    np.array([-0.2,0,1]),

    np.array([0,0.2,1]),

    np.array([0,-0.2,1])

]

for direction in directions:

    print("-"*50)

    print("Direction")
    print(direction)

    state = generator.generate(
        observer,
        direction
    )

    print()

    print("Initial State")

    print(state)

    print()

    print("Momentum")

    print("kt     =", state[4])
    print("kr     =", state[5])
    print("ktheta =", state[6])
    print("kphi   =", state[7])

