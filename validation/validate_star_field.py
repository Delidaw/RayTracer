import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


import numpy as np

from models.star_field import StarField


print("=" * 60)
print("STAR FIELD VALIDATION")
print("=" * 60)

star_field = StarField(
    "assets/milky_way.jpg"
)

test_directions = [
    np.array([1.0, 0.0, 0.0]),
    np.array([0.0, 1.0, 0.0]),
    np.array([-1.0, 0.0, 0.0]),
    np.array([0.0, -1.0, 0.0]),
    np.array([0.0, 0.0, 1.0]),
    np.array([0.0, 0.0, -1.0]),
]

for i, direction in enumerate(test_directions, start=1):

    colour = star_field.sample(direction)

    print(
        f"Direction {i}: "
        f"{direction} -> "
        f"colour = {colour}"
    )

print()
print("Texture size :", star_field.width, "x", star_field.height)
print("=" * 60)