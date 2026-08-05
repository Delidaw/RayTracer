import numpy as np
from concurrent.futures import ThreadPoolExecutor
from functools import partial

from rendering.background_sampler import BackgroundSampler
from rendering.disk_intersector import DiskIntersector
from rendering.disk_shader import DiskShader
from rendering.shadow_classifier import ShadowClassifier
from rendering.render_statistics import RenderStatistics
from rendering.photon_ring import PhotonRing
from rendering.frame_dragging import FrameDragging
from rendering.lensing_mapper import LensingMapper
from rendering.anti_aliasing import AntiAliasing
from rendering.hdr_buffer import HDRBuffer
from rendering.tone_mapper import ToneMapper
from rendering.bloom import Bloom
from rendering.gaussian_blur import GaussianBlur
from rendering.adaptive_sampler import AdaptiveSampler
from rendering.caustics import Caustics

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
        settings,
    ):

        self.scene = scene
        self.camera = camera
        self.ray_generator = ray_generator
        self.simulator = simulator
        self.settings = settings

        self.step_size = settings.step_size
        self.steps = settings.steps
        self.max_workers = settings.max_workers

        self.background = BackgroundSampler(
            scene.star_field
        )

        self.disk_intersector = DiskIntersector(
            scene.accretion_disk
        )

        self.disk_shader = DiskShader(
            scene.accretion_disk,
            scene.black_hole
        )

        self.shadow_classifier = ShadowClassifier()

        self.photon_ring = PhotonRing()

        self.frame_dragging = FrameDragging()

        self.lensing = LensingMapper()

        self.anti_aliasing = AntiAliasing()

        self.adaptive_sampler = AdaptiveSampler()

        self.tone_mapper = ToneMapper(
            exposure = settings.exposure
        )

        self.bloom = Bloom()

        self.blur = GaussianBlur()

        self.caustics = Caustics(
            scene.black_hole
        )

        self.statistics = RenderStatistics()


    def render(self):

        width = self.camera.width
        height = self.camera.height

        hdr = HDRBuffer(
            width,
            height
        )

        directions = self.camera.ray_directions()
        observer = self.camera.observer

        self.statistics.start()

        print()
        print("========== Stella Nova ==========")
        print(f"Rendering {width} x {height}")
        print()

        with ThreadPoolExecutor(
            max_workers = self.max_workers
        ) as executor:

            worker = partial(
                self.render_row,
                directions = directions,
                observer = observer,
            )

            results = executor.map(
                worker,
                range(height)
            )

            for row_index, colours in results:

                for j in range(width):

                    hdr.write(
                        row_index,
                        j,
                        colours[j]
                    )
            
        self.statistics.stop()

        self.statistics.summary(
            width,
            height
        )

        image = self.tone_mapper.map(
          hdr.image()
        )

        print("HDR min :", hdr.image().min())
        print("HDR max :", hdr.image().max())
        print("HDR mean :", hdr.image().mean())

        #print(hdr.image()[0,0])
        #print(hdr.image()[5,5])

        if self.settings.bloom:
            image = self.bloom.apply(image)

        if self.settings.blur:
            image = self.blur.apply(image)

        return image
        #return hdr.image()

    def render_row(self, 
                   row,
                   directions,
                   observer
                ):
        """
        Render a single image row
        using adaptive supersampling.
        """
        width = self.camera.width

        row_colours = np.zeros(
             (width, 3),
             dtype = np.float32
        )

        for j in range(width):

            # --------------------------------------------------
            # Primary centre ray
            # --------------------------------------------------

            direction = directions[row, j]
            """
            pixel += 1
        
            if pixel % 25 == 0 or pixel == total_pixels:
                print(
                    f"Progress : {pixel}/{total_pixels}"
                )
            """
        
            colour = self.trace_ray(
                direction,
                observer
            )

            # --------------------------------------------------
            # Decide how many samples this pixel needs
            # --------------------------------------------------

            samples = self.adaptive_sampler.samples(
                colour
            )

            # --------------------------------------------------
            # Smooth pixel: keep primary sample
            # --------------------------------------------------

            if samples == 1:

                row_colours[j] = colour

                continue

            # --------------------------------------------------
            # Edge / high-variance pixel:
            # trace centre + four subpixel samples
            # --------------------------------------------------

            sample_colours = [
                colour
            ]

            for offset_x, offset_y in self.adaptive_sampler.offsets[1:]:

                subpixel_x = j + offset_x
                subpixel_y = row + offset_y

                subpixel_direction = self.camera.ray_direction(
                    subpixel_x,
                    subpixel_y
                )

                subpixel_colour = self.trace_ray(
                    subpixel_direction,
                    observer
                )

                sample_colours.append(
                    subpixel_colour
                )

            # --------------------------------------------------
            # Average all samples
            # --------------------------------------------------

            row_colours[j] = np.mean(
                sample_colours,
                axis=0
            )

        return row, row_colours

    
    def trace_ray(self, direction, observer):
        """
        Trace a single photon ray and return its colour
        and classification.
        """

        state = self.ray_generator.generate(
            observer,
            direction
        )

        result = self.simulator.simulate(
            state,
            step_size=self.step_size,
            steps=self.steps
        )

        trajectory = result["trajectory"]

        if result["status"] == "numerical_error":

            return np.zeros(
                3,
                dtype=np.float32
            )

        # ---------------------------------------------
        # Black hole capture
        # ---------------------------------------------

        if self.shadow_classifier.is_shadow(result):

            self.statistics.record_capture()

            return np.array(
                [0.0, 0.0, 0.0],
                dtype=np.float32
            )

        # ---------------------------------------------
        # Accretion disk
        # ---------------------------------------------

        hit, hit_state = self.disk_intersector.intersects(
            trajectory
        )

        if hit:

            colour = self.disk_shader.shade(
                hit_state
            )

            boost = self.photon_ring.brightness(
                trajectory
            )

            boost *= self.frame_dragging.boost(
                trajectory
            )

            boost *= self.caustics.magnification(
                trajectory
            )

            colour = colour.astype(
                np.float32
            )

            colour *= boost

            self.statistics.record_disk_hit()

            return colour

        # ---------------------------------------------
        # Background / gravitationally lensed sky
        # ---------------------------------------------

        direction = self.lensing.direction(
            trajectory
        )

        colour = self.scene.star_field.sample(
            direction
        )

        self.statistics.record_background()

        return colour.astype(
            np.float32
        )