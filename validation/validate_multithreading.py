import sys
import os
import time

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

import numpy as np

from models.black_hole import BlackHole
from models.observer import Observer
from models.camera import Camera
from models.scene import Scene
from models.accretion_disk import AccretionDisk
from models.star_field import StarField

from physics.kerr_metric import KerrMetric
from physics.kerr_derivatives import KerrDerivatives
from physics.kerr_ray_generator import KerrRayGenerator
from physics.orbit_simulator import OrbitSimulator

from rendering.kerr_ray_tracer import KerrRayTracer


# ======================================================
# Configuration
# ======================================================

WIDTH = 5
HEIGHT = 5

STEPS = 20


# ======================================================
# Scene
# ======================================================

bh = BlackHole(
    mass=1.0,
    spin=0.9
)


metric = KerrMetric(bh)

derivatives = KerrDerivatives(
    metric
)

simulator = OrbitSimulator(
    metric,
    derivatives
)


observer = Observer(
    radius=20.0
)


disk = AccretionDisk(
    inner_radius=3.0,
    outer_radius=8.0,
    brightness=255
)


star_field = StarField(
    "assets/milky_way.jpg"
)


scene = Scene(
    black_hole=bh,
    observer=observer,
    star_field=star_field,
    accretion_disk=disk
)


camera = Camera(
    observer=observer,
    width=WIDTH,
    height=HEIGHT,
    fov=60
)


generator = KerrRayGenerator(
    metric
)


# ======================================================
# Single Worker
# ======================================================

print()
print("=" * 60)
print("SINGLE-WORKER RENDER")
print("=" * 60)

single_tracer = KerrRayTracer(
    scene,
    camera,
    generator,
    simulator,
    steps=STEPS,
    max_workers=1
)

start = time.time()

single_image = single_tracer.render()

single_time = time.time() - start


# ======================================================
# Multi Worker
# ======================================================

print()
print("=" * 60)
print("MULTI-WORKER RENDER")
print("=" * 60)

multi_tracer = KerrRayTracer(
    scene,
    camera,
    generator,
    simulator,
    steps=STEPS,
    max_workers=4
)

start = time.time()

multi_image = multi_tracer.render()

multi_time = time.time() - start


# ======================================================
# Compare Images
# ======================================================

difference = np.abs(
    single_image.astype(np.float64)
    -
    multi_image.astype(np.float64)
)

max_difference = difference.max()
mean_difference = difference.mean()


# ======================================================
# Results
# ======================================================

print()
print("=" * 60)
print("MULTITHREADING VALIDATION")
print("=" * 60)

print(
    f"Single-worker time : "
    f"{single_time:.4f} s"
)

print(
    f"Multi-worker time  : "
    f"{multi_time:.4f} s"
)

print(
    f"Speedup            : "
    f"{single_time / multi_time:.2f}x"
)

print(
    f"Maximum difference : "
    f"{max_difference:.10f}"
)

print(
    f"Mean difference    : "
    f"{mean_difference:.10f}"
)

print(
    f"Images identical   : "
    f"{np.allclose(single_image, multi_image)}"
)

print("=" * 60)