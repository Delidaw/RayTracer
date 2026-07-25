import numpy as np

from rendering.background_sampler import BackgroundSampler
from rendering.disk_intersector import DiskIntersector
from rendering.disk_shader import DiskShader
from rendering.shadow_classifier import ShadowClassifier

class KerrRayTracer:
    """
    Renders a Kerr black hole by tracing one photon 
    through every image pixel.
    """

    def __init__(
        self,
        scene,
        camera,
        ray_generator,
        simulator,
    ):
        self.scene = scene
        self.camera = camera
        self.ray_generator = ray_generator
        self.simulator = simulator

        self.background = BackgroundSampler(
            scene.star_field
        )

        self.disk_intersector = DiskIntersector(
            scene.accretion_disk
        )

        self.disk_shader = DiskShader(
            scene.accretion_disk
        )

        self.shadow_classifier = ShadowClassifier()
    """
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

                trajectory = result["trajectory"]

                if self.shadow_classifier.is_shadow(result):
                    image[j, i] = 0
                    
                hit, hit_state = self.disk_intersector.intersects(
                    trajectory
                )

                elif hit:
                    image[j, i] = self.disk_shader.shade(
                        hit_state
                    )

                else:
                    image[j, i] = self.background.sample(
                        trajectory[-1]
                    )

        return image
        """

    def render(self):

        width = self.camera.width
        height = self.camera.height

        print("Renderer started")

        image = np.zeros((height, width), dtype=np.uint8)

        print("Scene exists:", self.scene is not None)
        print("Camera:", width, "x", height)

        return image
    