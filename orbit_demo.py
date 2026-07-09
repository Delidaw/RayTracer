import numpy as np
import matplotlib.pyplot as plt

from models.black_hole import BlackHole
from physics.orbit_simulator import OrbitSimulator
from physics.initial_conditions import InitialConditions

#Create a blackhole
bh = BlackHole(mass = 10)

#create a simulator
simulator = OrbitSimulator(bh)

initials = InitialConditions(bh)

initial_state = initials.circular_orbit(radius = 50)

trajectory = simulator.simulate(
    initial_state,
    step_size = 0.05,
    steps = 5000
    )

r = trajectory[:, 1]
theta = trajectory[:, 2]
phi = trajectory[:, 3]

# Convert spherical coordinates to Cartesian for plotting
x = r * np.sin(theta) * np.cos(phi)
y = r * np.sin(theta) * np.sin(phi)
z = r * np.cos(theta)


plt.figure(figsize = (8, 8))

plt.plot(x, y)

plt.scatter(
    0,
    0,
    color = "black",
    s = 150,
    label = "Black Hole"
)

plt.xlabel("x")
plt.ylabel("y")

plt.axis("equal")

plt.grid(True)

plt.legend()

plt.title("Particle Orbit around a Schwarzschild Black Hole")

plt.show()