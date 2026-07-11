import numpy as np
import matplotlib.pyplot as plt

from models.black_hole import BlackHole
from physics.orbit_simulator import OrbitSimulator
from physics.initial_conditions import InitialConditions
from physics.particle_initial_conditions import ParticleInitialConditions

#Create a blackhole
bh = BlackHole(mass = 10)

#create a simulator
simulator = OrbitSimulator(bh)

particles = ParticleInitialConditions(bh)

initial_state = particles.radial_infall(radius=50)

step_size = 0.005

steps = 20000

trajectory = simulator.simulate(
    initial_state,
    step_size = step_size,
    steps = steps
    )

r = trajectory[:, 1]

time = np.arange(len(r)) * 0.005

"""
theta = trajectory[:, 2]
phi = trajectory[:, 3]

"""
print(f"Minimum radius : {np.min(r):.6f}")
print(f"Maximum radius : {np.max(r):.6f}")
print(f"Radius change  : {np.max(r) - np.min(r):.6f}")
"""

# Convert spherical coordinates to Cartesian for plotting
x = r * np.sin(theta) * np.cos(phi)
y = r * np.sin(theta) * np.sin(phi)
z = r * np.cos(theta)
"""

plt.figure(figsize = (10, 5))

plt.plot(time, r)



plt.xlabel("Proper Time")
plt.ylabel("Radius")

plt.title("Radial Infall")

plt.show()


print("First 10 radii:")
print(r[:10])

print("\nLast 10 radii:")
print(r[-10:])

print("\nFirst 10 radius differences:")
print(np.diff(r[:10]))

"""
print(f"Initial phi : {phi[0]}")
print(f"Final phi   : {phi[-1]}")
print(f"Total angle : {phi[-1] - phi[0]}")
print(phi[:10])
"""