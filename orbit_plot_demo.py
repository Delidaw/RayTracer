import numpy as np

from models.black_hole import BlackHole

from physics.kerr_metric import KerrMetric
from physics.kerr_derivatives import KerrDerivatives
from physics.orbit_simulator import OrbitSimulator

from visualization.orbit_plotter import OrbitPlotter

bh = BlackHole(
    mass=1.0,
    spin=0.5
)

metric = KerrMetric(bh)

derivatives = KerrDerivatives(metric)

simulator = OrbitSimulator(
    metric,
    derivatives
)

state = np.array([
    0.0,
    10.0,
    np.pi/2,
    0.0,

    1.0,
    0.0,
    0.0,
    0.05
])

result = simulator.simulate(
    state,
    step_size=0.01,
    steps=5000
)

trajectory = result["trajectory"]

plotter = OrbitPlotter()

plotter.plot(trajectory)