import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from physics.schwarzschild_metric import SchwarzschildMetric
from physics.photon_sphere import PhotonSphere
from models.black_hole import BlackHole

mass = 1.0

black_hole = BlackHole(mass)

metric = SchwarzschildMetric(black_hole)

photon_sphere = PhotonSphere(metric)

print("=" * 50)
print("Photon Sphere Validation")
print("=" * 50)

print(f"Mass M = {mass}")
print(f"Photon Sphere Radius = {photon_sphere.radius()}")

test_radii = [2.9, 3.0, 3.1]

for r in test_radii:
    print(f"\nr = {r}")
    print("Inside :", photon_sphere.is_inside(r))
    print("On     :", photon_sphere.is_on(r))
    print("Outside:", photon_sphere.is_outside(r))