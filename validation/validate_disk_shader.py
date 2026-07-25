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

for r in [3, 4, 5, 6, 7, 8]:

    state = np.array([
        0,
        r,
        np.pi/2,
        0,
        0,
        0,
        0,
        0
    ])

    print(
        f"r = {r:2}   brightness = {shader.shade(state)}"
    )