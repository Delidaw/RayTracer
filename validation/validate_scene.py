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
from models.scene import Scene
from models.star_field import StarField
from models.accretion_disk import AccretionDisk
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

stars = StarField()

disk = AccretionDisk(
    inner_radius=3,
    outer_radius=8
)

scene = Scene(
    black_hole = bh,
    observer = observer,
    star_field = stars,
    accretion_disk = disk
)

generator = KerrRayGenerator(metric)

tracer = KerrRayTracer(
    scene = scene,
    camera = camera,
    ray_generator = generator,
    simulator = simulator
)

image = tracer.render()

print(scene.black_hole)
print(scene.star_field)
print(scene.accretion_disk)

plt.figure(figsize = (6,6))

plt.imshow(
    image,
    cmap="gray",
    origin="lower"
)

plt.title("Kerr Ray Tracer Validation")

plt.axis("off")

plt.show()