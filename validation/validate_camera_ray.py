import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import matplotlib.pyplot as plt

from models.black_hole import BlackHole
from models.observer import Observer

from physics.schwarzschild_metric import SchwarzschildMetric
from physics.schwarzschild_derivatives import SchwarzschildDerivatives
from physics.observer_tetrad import ObserverTetrad
from physics.orbit_simulator import OrbitSimulator

from rendering.camera import Camera
from rendering.image_plane import ImagePlane
from rendering.ray_generator import RayGenerator
from rendering.ray_launcher import RayLauncher


black_hole = BlackHole(mass=1.0)

metric = SchwarzschildMetric(black_hole)

derivatives = SchwarzschildDerivatives(metric)

simulator = OrbitSimulator(
    metric,
    derivatives
)




observer = Observer(radius=20.0)

tetrad = ObserverTetrad(black_hole)

camera = Camera(
    width=800,
    height=800,
    fov=60
)

plane = ImagePlane(camera)

generator = RayGenerator(
    camera,
    plane
)

launcher = RayLauncher(
    observer,
    tetrad
)

pixels = [

    (400, 400),
    (500, 400),
    (600, 400),
    (700, 400),
    (799, 400)

]

print("=" * 70)
print("Camera Ray Validation")
print("=" * 70)

for px, py in pixels:

    print()
    print(f"Pixel ({px}, {py})")

    direction = generator.generate(px, py)

    print("Direction :", direction)

    state = launcher.launch(direction)

    print("kr     =", state[5])
    print("ktheta =", state[6])
    print("kphi   =", state[7])

    result = simulator.simulate(
        state,
        step_size=0.02,
        steps=30000
    )

    print("Status :", result["status"])

    trajectory = result["trajectory"]

    r = trajectory[:, 1]
    phi = trajectory[:, 3]

    x = r * np.cos(phi)
    y = r * np.sin(phi)

    plt.plot(
        x,
        y,
        label=f"{px}"
    )

plt.scatter(
    0,
    0,
    s=180,
    color="black",
    label="Black Hole"
)

plt.axis("equal")
plt.grid(True)
plt.legend(title="Pixel")

plt.show()