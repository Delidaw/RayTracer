import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np

from models.star_field import StarField
from rendering.background_sampler import BackgroundSampler

# Create a simple star field
stars = StarField()

# Create the sampler
sampler = BackgroundSampler(stars)

# Fake photon state
# [t, r, theta, phi, kt, kr, ktheta, kphi]
state = np.array([
    0.0,
    20.0,
    np.pi/2,
    0.0,
    1.0,
    -0.95,
    0.0,
    0.05
])

brightness = sampler.sample(state)

print("Brightness =", brightness)