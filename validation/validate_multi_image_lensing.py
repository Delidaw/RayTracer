import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

import numpy as np

from models.black_hole import BlackHole
from models.observer import Observer

from physics.kerr_metric import KerrMetric
from physics.kerr_derivatives import KerrDerivatives
from physics.kerr_ray_generator import KerrRayGenerator
from physics.orbit_simulator import OrbitSimulator

from rendering.lensing_mapper import LensingMapper


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
# Ray Generator
# ======================================================

generator = KerrRayGenerator(
    metric
)


# ======================================================
# Lensing Mapper
# ======================================================

lensing = LensingMapper()


# ======================================================
# Test rays
# ======================================================

ray_directions = [

    np.array([0.00, 0.00, 1.00]),

    np.array([0.02, 0.00, 0.9998]),

    np.array([0.04, 0.00, 0.9992]),

    np.array([0.06, 0.00, 0.9982]),

    np.array([0.00, 0.02, 0.9998]),

    np.array([0.00, 0.04, 0.9992]),

]


print()
print("=" * 60)
print("MULTI-IMAGE LENSING VALIDATION")
print("=" * 60)


escaped_directions = []


for i, camera_direction in enumerate(
    ray_directions,
    start=1
):

    camera_direction = (
        camera_direction /
        np.linalg.norm(camera_direction)
    )

    print()
    print("-" * 60)
    print(f"Ray {i}")
    print("-" * 60)

    print(
        "Initial direction :",
        camera_direction
    )

    state = generator.generate(
        observer,
        camera_direction
    )

    result = simulator.simulate(
        state,
        step_size=0.05,
        steps=500
    )

    trajectory = result["trajectory"]

    print(
        "Trajectory points :",
        len(trajectory)
    )

    # --------------------------------------------------
    # Final position
    # --------------------------------------------------

    final_state = trajectory[-1]

    print(
        "Final r           :",
        final_state[1]
    )

    print(
        "Final theta       :",
        final_state[2]
    )

    print(
        "Final phi         :",
        final_state[3]
    )

    # --------------------------------------------------
    # Map escaping trajectory to sky
    # --------------------------------------------------

    final_direction = lensing.direction(
        trajectory
    )

    print(
        "Final sky direction:",
        final_direction
    )

    escaped_directions.append(
        final_direction
    )


# ======================================================
# Angular separations
# ======================================================

print()
print("=" * 60)
print("ANGULAR SEPARATIONS")
print("=" * 60)


for i in range(
    len(escaped_directions)
):

    for j in range(i + 1, len(escaped_directions)):

        a = escaped_directions[i]
        b = escaped_directions[j]

        dot = np.clip(
            np.dot(a, b),
            -1.0,
            1.0
        )

        angle = np.arccos(dot)

        print(
            f"Ray {i + 1} ↔ Ray {j + 1} : "
            f"{angle:.8f} rad "
            f"({np.degrees(angle):.6f} deg)"
        )


print()
print("=" * 60)
print("VALIDATION COMPLETE")
print("=" * 60)