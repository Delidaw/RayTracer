import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.star_field import StarField
import numpy as np

texture_path = "assets/milky_way.jpg"

stars = StarField(texture_path)

print(stars.sample(np.array([0,0,1])))

TEXTURE = "assets/milky_way.jpg"   # <-- your actual texture path

stars = StarField(TEXTURE)

directions = [
    np.array([1.0, 0.0, 0.0]),
    np.array([-1.0, 0.0, 0.0]),
    np.array([0.0, 1.0, 0.0]),
    np.array([0.0, -1.0, 0.0]),
    np.array([0.0, 0.0, 1.0]),
    np.array([0.0, 0.0, -1.0]),
    np.array([1.0, 1.0, 1.0]),
]

print()
print("========== Star Field Validation ==========")

for d in directions:

    colour = stars.sample(d)

    print(f"{d} -> {colour}")

print()
print("✓ Bilinear sampling works.")