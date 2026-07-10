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

step_size = 0.005

orbital_period = simulator.orbital_period(initial_state)

total_time = 2 * orbital_period

steps = int(total_time / step_size)

trajectory = simulator.simulate(
    initial_state,
    step_size = step_size,
    steps = steps
    )

r = trajectory[:, 1]

# theta = trajectory[:, 2]
phi = trajectory[:, 3]

energy = []
angular_momentum = []

for state in trajectory:
    energy.append(bh.conserved_energy(state))
    angular_momentum.append(
        bh.conserved_angular_momentum(state)
    )

energy = np.array(energy)
angular_momentum = np.array(angular_momentum)

time = np.arange(len(r)) * step_size

"""
plt.figure(figsize = (10, 5))

plt.plot(time, r)

plt.xlabel("Proper Time")
plt.ylabel("Radius")

plt.title("Radius vs Proper Time")

plt.grid(True)

plt.show()
"""

"""
print(f"Initial phi : {phi[0]}")
print(f"Final phi   : {phi[-1]}")
print(f"Total angle : {phi[-1] - phi[0]}")
print(phi[:10])
"""

"""
plt.figure(figsize = (10, 5))

plt.plot(time,phi)

plt.xlabel("Proper Time")
plt.ylabel("Azimuthal Angle (φ)")

plt.title("Angular Position vs Proper Time")

plt.grid(True)

plt.show()
"""

plt.figure(figsize = (10, 5))

plt.plot(time, energy)

plt.xlabel("Proper Time")
plt.ylabel("Energy")

plt.title("Energy Conservation")

plt.grid(True)

plt.show()



plt.figure(figsize=(10,5))

plt.plot(time, angular_momentum)

plt.xlabel("Proper Time")
plt.ylabel("Angular Momentum")

plt.title("Angular Momentum Conservation")

plt.grid(True)

plt.show()