import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import matplotlib.pyplot as plt
import numpy as np

from models.black_hole import BlackHole
from physics.schwarzschild_metric import SchwarzschildMetric
from physics.schwarzschild_derivatives import SchwarzschildDerivatives
from physics.photon_initial_conditions import PhotonInitialConditions
from physics.orbit_simulator import OrbitSimulator

black_hole = BlackHole(mass = 1.0)

metric = SchwarzschildMetric(black_hole)

derivatives = SchwarzschildDerivatives(metric)

simulator = OrbitSimulator(
    metric,
    derivatives
)

photons = PhotonInitialConditions(black_hole)

epsilon = 1e-3

state_exact = photons.circular_photon_orbit(3.0)

state_outside = photons.circular_photon_orbit(3.0 + epsilon)

state_inside = photons.circular_photon_orbit(3.0 - 1e-3)

step_size = 0.01
steps = 200000

exact = simulator.simulate(
    state_exact,
    step_size,
    steps
)

outside = simulator.simulate(
    state_outside,
    step_size,
    steps
)

inside = simulator.simulate(
    state_inside,
    step_size,
    steps
)


#Polar to cartesian
traj_exact = exact["trajectory"]
traj_outside = outside["trajectory"]
traj_inside = inside["trajectory"]

x1 = traj_exact[:, 1] * np.cos(traj_exact[:, 3])
y1 = traj_exact[:, 1] * np.sin(traj_exact[:, 3])

x2 = traj_outside[:, 1] * np.cos(traj_outside[:, 3])
y2 = traj_outside[:, 1] * np.sin(traj_outside[:, 3])

x3 = traj_inside[:, 1] * np.cos(traj_inside[:, 3])
y3 = traj_inside[:, 1] * np.sin(traj_inside[:, 3])


print("Final radius (exact):", exact["trajectory"][-1, 1])
print("Final radius (outside):", outside["trajectory"][-1, 1])
print("Final radius (inside):", inside["trajectory"][-1, 1])

for name, result in [
    ("Exact", exact),
    ("Outside", outside),
    ("Inside", inside),
]:
    r = result["trajectory"][:, 1]
    print(f"{name}:")
    print("  r_min =", r.min())
    print("  r_max =", r.max())
    print()

plt.figure(figsize = (8,8))

plt.plot(x1, y1, label = "r = 3M")
plt.plot(x2, y2, label= "r = 3M + ε")
plt.plot(x3, y3, label= "r = 3M - ε")

plt.scatter(0, 0, s = 150, color = "black", label = "Black Hole")

plt.axis("equal")
plt.grid(True)
plt.legend()

plt.show()



print("Exact:")
print("Captured:", exact["captured"])
print("Escaped :", exact["escaped"])

print()

print("Outside:")
print("Captured:", outside["captured"])
print("Escaped :", outside["escaped"])

print()

print("Inside:")
print("Captured:", inside["captured"])
print("Escaped :", inside["escaped"])