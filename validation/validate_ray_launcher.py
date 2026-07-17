import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.black_hole import BlackHole

from models.observer import Observer
from physics.observer_tetrad import ObserverTetrad

from rendering.camera import Camera
from rendering.image_plane import ImagePlane
from rendering.ray_generator import RayGenerator
from rendering.ray_launcher import RayLauncher

black_hole = BlackHole(mass=1.0)

observer = Observer(radius=20.0)

tetrad = ObserverTetrad(black_hole)

camera = Camera(
    width=800,
    height=800,
    fov=60
)

plane = ImagePlane(camera)

generator = RayGenerator(camera, plane)

launcher = RayLauncher(
    observer,
    tetrad
)

direction = generator.generate(400, 400)

state = launcher.launch(direction)

print("=" * 60)
print("Camera Direction")
print("=" * 60)
print(direction)

print()

print("=" * 60)
print("Photon State")
print("=" * 60)
print(state)

print()

print("Coordinates")
print("t     =", state[0])
print("r     =", state[1])
print("theta =", state[2])
print("phi   =", state[3])

print()

print("Wave Vector")
print("kt     =", state[4])
print("kr     =", state[5])
print("ktheta =", state[6])
print("kphi   =", state[7])