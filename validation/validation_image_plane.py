import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from rendering.camera import Camera
from rendering.image_plane import ImagePlane

camera = Camera(
    width=800,
    height=800,
    fov=60
)

plane = ImagePlane(camera)

print("Plane Width :", plane.width)
print("Plane Height:", plane.height)