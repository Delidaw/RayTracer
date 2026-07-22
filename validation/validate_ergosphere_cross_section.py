import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import matplotlib.pyplot as plt

from models.black_hole import BlackHole
from physics.ergospgere import Ergosphere
from physics.event_horizon import EventHorizon

bh = BlackHole(
    mass = 1.0,
    spin = 0.9
)

ergo = Ergosphere(bh)

theta = np.linspace(
    0,
    np.pi,
    500 
)

r = ergo.radius(theta)

#Convert to Cartesian
x = r * np.sin(theta)
z = r * np.cos(theta)

#Mirror the left half
x_full = np.concatenate((-x[::-1], x))
z_full = np.concatenate((z[::-1], z))

plt.figure(figsize = (7,7))

"""
plt.plot(
    x_full,
    z_full,
    color = "purple",#by default if color not specified 
    linewidth = 2,#it is blue
    label = "Ergosphere"
)"""

plt.fill(
    x_full,
    z_full,
    color="lightskyblue",
    alpha=0.35,
    label="Ergosphere"
)

horizon = EventHorizon(bh)

R_h = horizon.radius()

plt.text(0.15, R_h + 0.05, "Event Horizon")

plt.text(0.7, 1.95, "Ergosphere")

xh = R_h * np.sin(theta)
zh = R_h * np.cos(theta)

xh_full = np.concatenate((-xh[::-1], xh))
zh_full = np.concatenate((zh[::-1], zh))
"""
plt.plot(
    xh_full,
    zh_full,
    color = "black",
    linewidth = 3,
    label = "Event Horizon"
)"""

plt.fill(
    xh_full,
    zh_full,
    color="black",
    label="Event Horizon"
)

plt.axvline(
    0,
    linestyle = "--",
    alpha = 0.6
)

plt.axis("equal")

plt.xlabel("x")
plt.ylabel("z")

plt.title(f"Kerr Black Hole (a = {bh.spin})")

plt.grid(True)

plt.legend()

plt.savefig(
    "outputs/kerr_ergosphere.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()