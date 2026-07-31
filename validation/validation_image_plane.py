import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.camera import Camera
from rendering.image_plane import ImagePlane
from models.observer import Observer

observer = Observer(radius = 50)

camera = Camera(
    observer = observer,
    width=800,
    height=800,
    fov=60
)

plane = ImagePlane(camera)

print("Plane Width :", plane.width)
print("Plane Height:", plane.height)