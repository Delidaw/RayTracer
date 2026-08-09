import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import matplotlib.pyplot as plt
import numpy as np

from models.black_hole import BlackHole
from models.observer import Observer
from models.camera import Camera
from models.scene import Scene
from models.accretion_disk import AccretionDisk

from physics.kerr_metric import KerrMetric
from physics.kerr_derivatives import KerrDerivatives
from physics.kerr_ray_generator import KerrRayGenerator
from physics.orbit_simulator import OrbitSimulator
from models.star_field import StarField

from rendering.kerr_ray_tracer import KerrRayTracer
from rendering.render_settings import RenderSettings

# ======================================================
# Render Settings
# ======================================================

settings = RenderSettings(
    width=10,
    height=10,
    fov=60,
    exposure=1.0,
    bloom=True,
    blur=True
)

# ======================================================
# Black Hole
# ======================================================

bh = BlackHole(
    mass=1.0,
    spin=0.9
)


# ======================================================
# Physics
# ======================================================

metric = KerrMetric(bh)

derivatives = KerrDerivatives(metric)

simulator = OrbitSimulator(
    metric,
    derivatives
)


# ======================================================
# Observer
# ======================================================

observer = Observer(
    radius=20.0
)


# ======================================================
# Accretion Disk
# ======================================================

disk = AccretionDisk(
    inner_radius=3.0,
    outer_radius=8.0,
    brightness=255
)

# ======================================================
# Star Field
# ======================================================

star_field = StarField(
    "assets/milky_way.jpg"
)

direction = np.array([1.0, 0.0, 0.0])

print(type(star_field.sample(direction)))
print(star_field.sample(direction))

# ======================================================
# Scene
# ======================================================

scene = Scene(
    black_hole=bh,
    observer=observer,
    star_field=star_field,
    accretion_disk=disk
)


# ======================================================
# Camera
# ======================================================

camera = Camera(
    observer=observer,
    width=settings.width,      # Increase later
    height=settings.height,
    fov=settings.fov
)

directions = camera.ray_directions()

centre = directions[
    camera.height // 2,
    camera.width // 2
]

print("\n========== Centre Camera Ray ==========")
print(centre)


# ======================================================
# Ray Generator
# ======================================================

generator = KerrRayGenerator(
    metric
)

print("\n========== Centre Photon ==========")

state = generator.generate(
    observer,
    centre
)

print(state)


# ======================================================
# Renderer
# ======================================================

tracer = KerrRayTracer(
    scene,
    camera,
    generator,
    simulator,
    settings
)


# ======================================================
# Render
# ======================================================
print("Before render")
direction = np.array([1.0, 0.0, 0.0])
print(type(star_field.sample(direction)))
print(star_field.sample(direction))
print("Calling render...")

image = tracer.render()


# ======================================================
# Display
# ======================================================

"""
plt.imshow(
    image,
    origin="lower"
)
"""
plt.imshow(np.clip(image / 255.0, 0, 1))

plt.title("Photon Forge - First Kerr Render")

plt.axis("off")

plt.show()