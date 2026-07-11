import numpy as np
import matplotlib.pyplot as plt

from models.black_hole import BlackHole

from physics.orbit_simulator import OrbitSimulator
from physics.photon_initial_conditions import PhotonInitialConditions

#creating the simulator
bh = BlackHole(mass=1)

simulator = OrbitSimulator(bh)

photons = PhotonInitialConditions(bh)

#launching many photons
impact_parameters = [
    2,
    3,
    4,
    5,
    6,
    8,
    10
]

plt.figure(figsize=(8, 8))

for b in impact_parameters:
    
    initial = photons.light_ray(
        radius = 50,
        impact_parameter = b
    )

    trajectory = simulator.simulate(
        initial,
        step_size = 0.01,
        steps = 12000
    )

    print("kphi initial =", trajectory[0,7])
    print("kphi final   =", trajectory[-1,7])

    print("phi first 10 values")
    print(trajectory[:10,3])

    r = trajectory[:, 1]
    phi = trajectory[:, 3]

    x = r * np.cos(phi)
    y = r * np.sin(phi)

    plt.plot(
        x,
        y,
        label=f"b={b}"
    )

#black hole draw
plt.scatter(
   0,
   0,
   s=200,
   color="black",
   label="Black Hole"
)


#Draw the event horizon
plt.gca().add_patch(

    plt.Circle(
        (0,0),
        bh.schwarzschild_radius,
        color="black",
        alpha=0.3
    )
)

#Draw the photon sphere

plt.gca().add_patch(

    plt.Circle(
        (0,0),
        bh.photon_sphere,
        fill=False,
        color="orange",
        linestyle="--",
        linewidth=2,
        label="Photon Sphere"
    )
)

plt.gca().set_aspect("equal")

plt.xlabel("x")

plt.ylabel("y")

plt.title("Gravitational Light Bending")

plt.grid(True)

plt.legend()

plt.show()


print("x min:", np.min(x))
print("x max:", np.max(x))

print("y min:", np.min(y))
print("y max:", np.max(y))


print("r min:", np.min(r))
print("r max:", np.max(r))

print("phi min:", np.min(phi))
print("phi max:", np.max(phi))