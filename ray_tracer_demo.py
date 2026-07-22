import matplotlib.pyplot as plt
import physics.orbit_simulator as sim

print(sim.__file__)

from models.black_hole import BlackHole
from models.observer import Observer
from models.camera import Camera

from rendering.schwarzschild_ray_tracer import SchwarzschildRayTracer
import physics.ray_generator as rg

print("RayGenerator file:")
print(rg.__file__)
bh = BlackHole(mass=1)

observer = Observer(radius=50)

camera = Camera(
    observer,
    width=5,#2500 Rays
    height=5
)

renderer = SchwarzschildRayTracer(
    bh,
    camera
)

try:
    image = renderer.render()
except Exception as e:
    import traceback
    traceback.print_exc()

    raise

plt.imshow(image, interpolation="nearest")

plt.axis("off")

plt.show()