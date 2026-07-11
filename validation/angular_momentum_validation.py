import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))



import numpy as np

from models.black_hole import BlackHole
from physics.initial_conditions import InitialConditions
from physics.orbit_simulator import OrbitSimulator

bh = BlackHole(mass=1)

initial = InitialConditions(bh).circular_orbit(radius=10)

simulator = OrbitSimulator(bh)

trajectory = simulator.simulate(
    initial,
    step_size=0.01,
    steps=10000
)

L = np.array([
    bh.conserved_angular_momentum(state)
    for state in trajectory
])

print("Initial L :", L[0])
print("Final L   :", L[-1])
print("Minimum L :", L.min())
print("Maximum L :", L.max())
print("L Drift   :", L.max() - L.min())