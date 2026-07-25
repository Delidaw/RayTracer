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

                direction = directions[j, i]

                state = self.ray_generator.generate(
                    observer,
                    direction
                )

                result = self.simulator.simulate(
                    state,
                    step_size = 0.05,
                    steps = 300
                )

                if result["captured"]:
                    image[j, i] = 0
                else:
                    image[j, i] = 255

        return image