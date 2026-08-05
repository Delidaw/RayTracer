import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np

from rendering.photon_ring import PhotonRing


ring = PhotonRing()

print()
print("=" * 60)
print("PHOTON RING VALIDATION")
print("=" * 60)


def make_trajectory(total_angle, points=200):
    """
    Create a fake trajectory with a specified
    total azimuthal rotation.
    """

    trajectory = np.zeros((points, 8), dtype=np.float64)

    trajectory[:, 3] = np.linspace(
        0.0,
        total_angle,
        points
    )

    return trajectory


tests = [
    ("Straight ray", 0.2),
    ("Quarter orbit", 0.5 * np.pi),
    ("Half orbit", np.pi),
    ("One orbit", 2.0 * np.pi),
    ("Two orbits", 4.0 * np.pi),
    ("Three orbits", 6.0 * np.pi),
]


for name, angle in tests:

    trajectory = make_trajectory(angle)

    boost = ring.brightness(trajectory)

    print(f"{name:<15} : {boost:.3f}")


print()
print("=" * 60)
print("VALIDATION COMPLETE")
print("=" * 60)