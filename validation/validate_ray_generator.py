import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.camera import Camera
from rendering.image_plane import ImagePlane
from rendering.ray_generator import RayGenerator
from models.observer import Observer

# ------------------------
# Build rendering pipeline
# ------------------------

observer = Observer(radius = 50)
camera = Camera(
    observer = observer,
    width=800,
    height=800,
    fov=60
)

image_plane = ImagePlane(camera)

generator = RayGenerator(
    camera,
    image_plane
)

# ------------------------
# Test rays
# ------------------------

center = generator.generate(400, 400)

top_left = generator.generate(0, 0)

bottom_right = generator.generate(799, 799)

print("Center       :", center)
print("Top Left     :", top_left)
print("Bottom Right :", bottom_right)