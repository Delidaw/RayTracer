import numpy as np
import matplotlib.pyplot as plt

from models.black_hole import BlackHole
from physics.orbit_simulator import OrbitSimulator
from physics.photon_initial_conditions import PhotonInitialConditions

# Create black hole
bh = BlackHole(mass=10)

# Create simulator
simulator = OrbitSimulator(bh)

# Photon initial conditions
photons = PhotonInitialConditions(bh)

initial_state = photons.radial_ray(
    radius = 50,
    inward = True
)

trajectory = simulator.simulate(
    initial_state,
    step_size = 0.005,
    steps = 5000
)

r = trajectory[:, 1]
theta = trajectory[:, 2]
phi = trajectory[:, 3]

#Converting to Cartesian coordinates
x = r * np.sin(theta) * np.cos(phi)
y = r * np.sin(theta) * np.sin(phi)

plt.figure(figsize = (8, 8))

plt.plot(x, y, label = "Photon")

plt.scatter(
    0,
    0,
    color = "black",
    s = 150,
    label = "Black Hole"
)

plt.gca().set_aspect("equal")

plt.xlabel("x")
plt.ylabel("y")

plt.title("Radial Photon Trajectory")

plt.grid(True)
plt.legend()

plt.show()

print("Initial radius :", trajectory[0,1])
print("Final radius   :", trajectory[-1,1])

print("Minimum radius :", trajectory[:,1].min())
print("Maximum radius :", trajectory[:,1].max())