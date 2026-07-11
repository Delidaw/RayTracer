from models.observer import Observer
from models.camera import Camera

observer = Observer(radius = 50)

camera = Camera(
    observer,
    fov = 60,
    width = 5,
    height = 5
)

X, Y = camera.pixel_grid()

print(X)
print()
print(Y)
