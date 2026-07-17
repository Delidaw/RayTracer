import numpy as np
import matplotlib.pyplot as plt

from models.black_hole import BlackHole

from physics.orbit_simulator import OrbitSimulator
from physics.photon_initial_conditions import PhotonInitialConditions

bh = BlackHole(mass=1)

simulator = OrbitSimulator(bh)

photons = PhotonInitialConditions(bh)

initial = photons.light_ray(
    radius = 50,
    impact_parameter = 8
)

trajectory = simulator.simulate(
    initial, 
    step_size = 0.01,
    steps = 6000
)

r = trajectory[:, 1]
kt = trajectory[:, 4]
kr = trajectory[:, 5]
kphi = trajectory[:, 7]

R_s = bh.schwarzschild_radius

f = 1 - R_s / r

null_condition = (
    -f * kt **2
    + (kr ** 2) / f
    + r**2 * kphi **2
)

plt.figure(figsize=(8, 5))

plt.plot(
    null_condition,
    linewidth = 2
)

plt.axhline(
    0,
    color = "red",
    linestyle = "--"
)

plt.xlabel("Integration step")

plt.ylabel(r"$g_{\mu\nu}k^\mu k^\nu$")
plt.title("Null Geodesic Validation")

plt.grid(True)

plt.show()

print()

print("Minimum :", np.min(null_condition))

print("Maximum :", np.max(null_condition))

print("Mean    :", np.mean(null_condition))