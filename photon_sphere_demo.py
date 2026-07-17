import numpy as np
import matplotlib.pyplot as plt

from models.black_hole import BlackHole
from physics.orbit_simulator import OrbitSimulator
from physics.photon_initial_conditions import PhotonInitialConditions

bh = BlackHole(mass = 1)

simulator = OrbitSimulator(bh)

photons = PhotonInitialConditions(bh)


#for M = 1, b = 3root3 M = 5.196
impact_parameters = [
    4.8,  #-->captured
    5.196,#-->crtical photon orbit
    5.6   #-->escapes after bending
]

for b in impact_parameters:

    initial = photons.light_ray(
        radius = 50,
        impact_parameter=b
    )

    trajectory = simulator.simulate(
        initial, step_size = 0.01,
        steps = 25000
    )

    r = trajectory[:, 1]
    phi = trajectory[:, 3]

    x = r * np.cos(phi)
    y = r * np.sin(phi)

    plt.plot(
        x,
        y,
        linewidth = 2,
            label = f"b = {b:.3f}"
    )

#blackhole drawing
plt.gca().add_patch(
    plt.Circle(
        (0, 0),
        bh.schwarzschild_radius,
        color="black",
        alpha = 0.4
    )
)

#photon sphere drawing
plt.gca().add_patch(
    plt.Circle(
        (0, 0),
        bh.photon_sphere,
        fill = False,
        color = "red",
        linestyle = "--",
        linewidth = 2,
        label = "Photon Sphere"
    )
)

plt.scatter(
    0,
    0,
    color = "black",
    s = 100
)

plt.gca().set_aspect("equal")

plt.xlabel("x")
plt.ylabel("y")

plt.title("Photon Sphere Demonstration")

plt.grid(True)

plt.legend()

plt.show()