import numpy as np

from models.black_hole import BlackHole
from physics.schwarzschild_metric import SchwarzschildMetric
from physics.schwarzschild_derivatives import SchwarzschildDerivatives
from physics.photon_initial_conditions import PhotonInitialConditions
from physics.orbit_simulator import OrbitSimulator


def simulate_circular_photon(
    radius=3.0,
    mass=1.0,
    step_size=0.01,
    steps=200000
):

    # Build engine
    black_hole = BlackHole(mass=mass)

    metric = SchwarzschildMetric(black_hole)

    derivatives = SchwarzschildDerivatives(metric)

    simulator = OrbitSimulator(
        metric,
        derivatives
    )

    photons = PhotonInitialConditions(black_hole)

    # Initial state
    state = photons.circular_photon_orbit(radius)

    # Run simulation
    result = simulator.simulate(
        state,
        step_size,
        steps
    )

    traj = result["trajectory"]

    # Polar → Cartesian
    x = traj[:, 1] * np.cos(traj[:, 3])
    y = traj[:, 1] * np.sin(traj[:, 3])

    return {
        "x": x.tolist(),
        "y": y.tolist(),
        "captured": result["captured"],
        "escaped": result["escaped"]
    }