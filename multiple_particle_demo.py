import numpy as np
import matplotlib.pyplot as plt

from models.black_hole import BlackHole

from physics.initial_conditions import InitialConditions
from physics.orbit_simulator import OrbitSimulator
from physics.particle_ensemble import ParticleEnsemble

bh = BlackHole(mass=1)

initial = InitialConditions(bh)

simulator = OrbitSimulator(bh)

ensemble = ParticleEnsemble(simulator)

ensemble.add_particle(
    "Circular Orbit",
    initial.circular_orbit(radius = 10)
)

ensemble.add_particle(
    "Radial Infall",
    initial.radial_infall(radius = 20)
)

ensemble.add_particle(
    "Escape Trajectory",
    initial.escape_trajectory(
        radius = 20,
        radial_velocity = 0.2,
        angular_velocity = 0.02
    )
)

ensemble.add_particle(
    "Elliptical Orbit",
    initial.elliptical_orbit(
        semi_major_axis = 20,
        eccentricity = 0.4
    )
)

trajectories = ensemble.simulate_all(
    step_size=0.01,
    steps=30000
)

#Plotting all

plt.figure(figsize=(8, 8))

for result in trajectories:

    trajectory = result["trajectory"]
    label = result["name"]

    r = trajectory[:, 1]
    phi = trajectory[:, 3]

    x = r * np.cos(phi)
    y = r * np.sin(phi)

    plt.plot(x, y, label=label)


#Drawing the black hole

R_s = bh.schwarzschild_radius

plt.gca().add_patch(
    plt.Circle(
        (0, 0),
        R_s,
        color="black",
        alpha=0.3,
        label="Event Horizon"
    )
)

plt.scatter(
    0, 
    0,
    color ="black",
    s = 80
)

plt.gca().set_aspect("equal")

plt.xlabel("x")
plt.ylabel("y")

plt.title("Multiple Particle Simulation")

plt.grid(True)

plt.legend()

plt.show()