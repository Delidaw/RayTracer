import sys
import os

# ======================================================
# Project Root
# ======================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, PROJECT_ROOT)


# ======================================================
# Imports
# ======================================================

import matplotlib.pyplot as plt
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
from rendering.animation_engine import AnimationEngine
from rendering.animation_exporter import AnimationExporter

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

derivatives = KerrDerivatives(
    metric
)

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
    width=5,
    height=5,
    fov=60
)


# ======================================================
# Ray Generator
# ======================================================

generator = KerrRayGenerator(
    metric
)


# ======================================================
# Kerr Ray Tracer
# ======================================================

tracer = KerrRayTracer(
    scene,
    camera,
    generator,
    simulator,
    steps=20
)


# ======================================================
# Animation Engine
# ======================================================

animation = AnimationEngine(
    tracer=tracer,
    camera=camera,
    frames=3
)


# ======================================================
# Render Animation Frames
# ======================================================

print()
print("=" * 50)
print("Starting Stella Nova Animation")
print("=" * 50)

frames = animation.render_frames()

# ======================================================
# Export Animation
# ======================================================

exporter = AnimationExporter(
    fps=2
)

exporter.save_gif(
    frames,
    "stella_nova_animation.gif"
)

exporter.save_mp4(
    frames,
    "stella_nova_animation.mp4"
)

print()
print("=" * 50)
print("CAMERA MOTION VALIDATION")
print("=" * 50)

for frame in range(3):
    phi = (
        2.0 * np.pi *
        frame /
        animation.frames
    )

    print(
        f"Frame {frame + 1}: "
        f"phi = {phi:.6f} rad"
    )


# ======================================================
# Validation Results
# ======================================================

print()
print("=" * 50)
print("ANIMATION VALIDATION")
print("=" * 50)

print(
    "Number of frames :",
    len(frames)
)

for i, frame in enumerate(frames):

    print(
        f"Frame {i + 1}: "
        f"shape={frame.shape}, "
        f"min={frame.min():.6f}, "
        f"max={frame.max():.6f}"
    )


# ======================================================
# Display Last Frame
# ======================================================

plt.imshow(
    np.clip(
        frames[-1] / 255.0,
        0,
        1
    )
)

plt.title(
    "Stella Nova - Animation Frame 3"
)

plt.axis("off")

plt.show()