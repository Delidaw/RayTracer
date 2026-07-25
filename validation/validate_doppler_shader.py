import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np

from models.accretion_disk import AccretionDisk
from rendering.disk_shader import DiskShader

disk = AccretionDisk(
    inner_radius=3,
    outer_radius=8
)

shader = DiskShader(disk)

for phi in np.linspace(0, 2*np.pi, 9):

    state = np.array([
        0,
        5,
        np.pi/2,
        phi,
        0,
        0,
        0,
        0
    ])

    print(
        f"{phi:.2f}",
        shader.shade(state)
    )