import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import matplotlib.pyplot as plt

from models.star_field import StarField


TEXTURE = "assets/milky_way.jpg"

stars = StarField(TEXTURE)

height = 300
width = 600

image = np.zeros((height, width, 3), dtype=np.uint8)

for i in range(height):

    theta = np.pi * i / (height - 1)

    for j in range(width):

        phi = 2 * np.pi * j / (width - 1) - np.pi

        direction = np.array([
            np.cos(phi) * np.sin(theta),
            np.sin(phi) * np.sin(theta),
            np.cos(theta)
        ])

        image[i, j] = stars.sample(direction)

plt.imshow(image)
plt.title("StarField Sampling Validation")
plt.axis("off")
plt.show()