import sys
import os

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, PROJECT_ROOT)

from models.observer import Observer
from rendering.camera_paths import (
    OrbitPath,
    ZoomPath,
    SpiralPath,
)

observer = Observer(radius=20.0)

paths = [
    OrbitPath(),
    ZoomPath(),
    SpiralPath(),
]

print()
print("=" * 60)
print("CAMERA PATH VALIDATION")
print("=" * 60)

for path in paths:

    print(f"\n{path.__class__.__name__}")

    observer.radius = 20.0
    observer.phi = 0.0

    for frame in [0, 5, 9]:

        path.update(
            observer,
            frame,
            10
        )

        print(
            f"Frame {frame:2d}"
            f"  radius={observer.radius:.3f}"
            f"  phi={observer.phi:.3f}"
        )

print()
print("=" * 60)
print("VALIDATION COMPLETE")
print("=" * 60)