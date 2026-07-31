import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np

from models.black_hole import BlackHole
from rendering.caustics import Caustics


black_hole = BlackHole(
    mass=1.0,
    spin=0.9
)

caustics = Caustics(black_hole)


def trajectory(r_values):
    traj = np.zeros((len(r_values), 8))
    traj[:, 1] = r_values
    return traj


tests = [
    ("Far away", [20, 15, 10, 8]),
    ("Moderately close", [20, 8, 5, 4]),
    ("Near photon region", [20, 6, 3.5, 2.8]),
    ("Very close", [20, 4, 2.4, 2.1]),
]

print("\n========== Caustics Validation ==========\n")

for name, radii in tests:

    boost = caustics.magnification(
        trajectory(radii)
    )

    print(f"{name:20s}: {boost:.3f}")

print("\n✓ Caustics validation complete.")