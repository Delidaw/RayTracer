import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

import numpy as np

from models.observer import Observer
from models.camera import Camera


observer = Observer(
    radius=20.0
)

camera = Camera(
    observer=observer,
    width=10,
    height=10,
    fov=60
)


print()
print("========== Camera Subpixel Validation ==========")

positions = [
    (5.0, 5.0),
    (4.75, 4.75),
    (5.25, 4.75),
    (4.75, 5.25),
    (5.25, 5.25)
]

for x, y in positions:

    direction = camera.ray_direction(
        x,
        y
    )

    print(
        f"Pixel ({x}, {y}) -> "
        f"{direction}"
    )

    print(
        "Norm =",
        np.linalg.norm(direction)
    )