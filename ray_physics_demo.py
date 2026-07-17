import numpy as np

from models.black_hole import BlackHole
from physics.ray_physics import RayPhysics

bh = BlackHole(mass=1)

physics = RayPhysics(bh)

radii = [
    2.2,
    3,
    5,
    10,
    20,
    50
]

print()

print("Ray Physics Demonstration")
print("-" * 50)

for r in radii:

    print(f"\nRadius = {r:.2f}")

    print(
        f"Redshift          : {physics.redshift(r):.6f}"
    )

    print(
        f"Escape Velocity   : {physics.escape_velocity(r):.6f}"
    )

    print(
        f"Orbital Velocity  : {physics.orbital_velocity(r):.6f}"
    )

    print(
        f"Lensing Strength  : {physics.lensing_strength(r):.6f}"
    )