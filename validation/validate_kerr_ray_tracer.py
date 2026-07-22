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

derivatives = KerrDerivatives(metric)

simulator = OrbitSimulator(
    metric,
    derivatives
)

observer = Observer(
    radius=20.0
)

camera = Camera(
    observer=observer,
    width=30,
    height=30,
    fov=60
)

generator = KerrRayGenerator(metric)

tracer = KerrRayTracer(
    camera,
    generator,
    simulator
)

image = tracer.render()

plt.imshow(
    image,
    cmap="gray",
    origin="lower"
)

plt.show()