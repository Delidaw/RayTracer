import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))


import numpy as np
import matplotlib.pyplot as plt

from models.black_hole import BlackHole
from physics.initial_conditions import InitialConditions
from physics.orbit_simulator import OrbitSimulator

bh = BlackHole(mass = 1)

initial = InitialConditions(bh).circular_orbit(radius = 10)

simulator = OrbitSimulator(bh)

trajectory = simulator.simulate(
    initial,
    step_size = 0.01,
    steps = 10000
)

energies = np.array([
    bh.conserved_energy(state)
    for state in trajectory
])

print("Initial Energy :", energies[0])
print("Final Energy   :", energies[-1])
print("Minimum Energy :", energies.min())
print("Maximum Energy :", energies.max())
print("Energy Drift   :", energies.max() - energies.min())