import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np

from models.black_hole import BlackHole
from physics.schwarzschild_metric import SchwarzschildMetric
from physics.schwarzschild_derivatives import SchwarzschildDerivatives
from physics.photon_initial_conditions import PhotonInitialConditions
from physics.orbit_simulator import OrbitSimulator
from physics.impact_parameter import ImpactParameter

# ---------------------------------------
# Build Physics Engine
# ---------------------------------------

black_hole = BlackHole(mass=1.0)

metric = SchwarzschildMetric(black_hole)

derivatives = SchwarzschildDerivatives(metric)

simulator = OrbitSimulator(
    metric,
    derivatives
)

photons = PhotonInitialConditions(black_hole)

impact = ImpactParameter(black_hole)

bc = impact.critical()

print("=" * 60)
print("Critical Impact Parameter Validation")
print("=" * 60)

print(f"Theoretical b_c = {bc:.10f}")
print()

impact_parameters = [

    4.5,
    4.8,
    5.0,
    5.1,
    5.15,
    5.18,
    5.19,
    5.195,
    5.196,
    5.197,
    5.20,
    5.25,
    5.3,
    5.5,
    6.0
]

start_radius = 50.0

step_size = 0.02

steps = 30000

escape_radius = 100.0

print("{:<15} {:<15}".format(
    "Impact Parameter",
    "Status"
))

print("-" * 30)

for b in impact_parameters:

    # Generate photon
    initial_state = photons.light_ray(
        start_radius,
        b
    )

    # Simulate trajectory
    result = simulator.simulate(
        initial_state,
        step_size,
        steps,
        escape_radius=escape_radius
    )

    # Print result
    print(
        "{:<15.6f} {:<15}".format(
            b,
            result["status"]
        )
    )