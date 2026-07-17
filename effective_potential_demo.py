import numpy as np
import matplotlib.pyplot as plt

from models.black_hole import BlackHole
from physics.effective_potential import EffectivePotential

bh = BlackHole(mass=1)

potential = EffectivePotential(bh)

L = 4
r = np.linspace(2.1, 40, 1000)

V = potential.particle(r, L)

plt.figure(figsize=(8,6))

plt.plot(r, V)

plt.axvline(
    bh.schwarzschild_radius,
    color="red",
    linestyle="--",
    label="Event Horizon"
)

plt.axvline(
    bh.photon_sphere,
    color="orange",
    linestyle="--",
    label="Photon Sphere"
)

plt.axvline(
    bh.isco,
    color="green",
    linestyle="--",
    label="ISCO"
)

plt.axvspan(
    0,
    bh.schwarzschild_radius,
    color="black",
    alpha=0.12
)

plt.scatter(
    bh.photon_sphere,
    potential.particle(bh.photon_sphere, L),
    color="orange",
    s=80,
    zorder=5
)

plt.scatter(
    bh.isco,
    potential.particle(bh.isco, L),
    color="green",
    s=80,
    zorder=5
)

plt.xlabel("Radius")

plt.ylabel("Effective Potential")

plt.title("Schwarzschild Particle Effective Potential")

plt.grid(True)
plt.legend()

plt.show()