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
# Ray Generator
# ======================================================

generator = KerrRayGenerator(
    metric
)

lensing = LensingMapper()


print()
print("=" * 70)
print("STRONG LENSING VALIDATION")
print("=" * 70)

# Scan across the camera horizontally
x_values = np.linspace(
    -0.35,
    0.35,
    21
)

for x in x_values:

    direction = np.array(
        [x, 0.0, 1.0],
        dtype=np.float64
    )

    direction /= np.linalg.norm(direction)

    state = generator.generate(
        observer,
        direction
    )

    result = simulator.simulate(
        state,
        step_size=0.05,
        steps=100
    )

    trajectory = result["trajectory"]

    r_min = np.min(
        trajectory[:, 1]
    )

    final_r = trajectory[-1, 1]

    print("final r  :", final_r)
    print("final kr :", trajectory[-1, 5])

    escaped = final_r > observer.radius

    print(
        f"x={x:+.3f} | "
        f"r_min={r_min:6.3f} | "
        f"final_r={final_r:7.3f} | "
        f"{'ESCAPED' if escaped else 'CAPTURED'}"
    )

    if escaped:

        sky = lensing.direction(
            trajectory
        )

        print(
            "   Final sky direction:",
            np.round(sky, 5)
        )

print()
print("=" * 70)
print("VALIDATION COMPLETE")
print("=" * 70)