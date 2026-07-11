from models.observer import Observer
from models.camera import Camera

observer = Observer(radius=50)

camera = Camera(
    observer,
    width = 3,
    height = 3,
    fov = 60
)

rays = camera.ray_directions()

print(rays)