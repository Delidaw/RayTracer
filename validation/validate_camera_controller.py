import sys
import os

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, PROJECT_ROOT)

from models.observer import Observer
from models.camera import Camera

from rendering.camera_paths import OrbitPath
from rendering.camera_controller import CameraController

observer = Observer(radius=20.0)

camera = Camera(
    observer=observer,
    width=100,
    height=100,
    fov=60
)

controller = CameraController(
    camera,
    OrbitPath()
)

print()
print("=" * 60)
print("CAMERA CONTROLLER VALIDATION")
print("=" * 60)

for frame in [0, 5, 9]:

    controller.update(
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