import numpy as np

class KerrRayTracer:
    """
    Renders a Kerr black hole by tracing one photon 
    through every image pixel.
    """

    def __init__(
            self,
            camera,
            ray_generator,
            simulator
        ):
        self.camera = camera
        self.ray_generator = ray_generator
        self.simulator = simulator

    def render(self):
        width = self.camera.width
        height = self.camera.height

        image = np.zeros(
            (height, width),
            dtype = np.uint8
        )

        directions = self.camera.ray_directions()
        observer = self.camera.observer

        for i in range(height):
            for j in range(width):

                direction = directions[i, j]

                state = self.ray_generator.generate(
                    observer,
                    direction
                )

                result = self.simulator.simulate(
                    state,
                    step_size = 0.01,
                    steps = 5000
                )

                if result["captured"]:
                    image[i, j] = 0
                else:
                    image[i, j] = 255

        return image