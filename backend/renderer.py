import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import matplotlib.pyplot as plt
import numpy as np

from models.black_hole import BlackHole
from models.observer import Observer
from models.camera import Camera
from models.scene import Scene
from models.accretion_disk import AccretionDisk

from physics.kerr_metric import KerrMetric
from physics.kerr_derivatives import KerrDerivatives
from physics.kerr_ray_generator import KerrRayGenerator
from physics.orbit_simulator import OrbitSimulator
from models.star_field import StarField

from rendering.kerr_ray_tracer import KerrRayTracer
from rendering.render_settings import RenderSettings


def render_black_hole(parameters):
    """
    Render one black hole image using the
    existing Photon Forge pipeline.
    """

    #
    # We'll build everything here
    #


    # ======================================================
    # Render Settings
    # ======================================================

    resolution = parameters("resolution", 64)

    steps = int(
        parameters.get("steps", 20)
    )

    fov = float(
        parameters.get("fov", 55.0)
    )

    settings = RenderSettings(
        width=resolution,
        height = resolution,
        fov=fov,
        exposure=1.0,
        bloom=True,
        blur=True,
        steps = steps,
        step_size = 0.05,
        max_workers = 4
    )

    # ======================================================
    # Black Hole
    # ======================================================
    
    mass = float(parameters.get("mass", 1.0))
    spin = float(parameters.get("spin", 0.9))
                 
    observer_radius = parameters("observer_radius", 20.0)
    

    bh = BlackHole(
        mass=mass,
        spin=spin
    )


    # ======================================================
    # Physics
    # ======================================================

    metric = KerrMetric(bh)

    derivatives = KerrDerivatives(metric)

    simulator = OrbitSimulator(
        metric,
        derivatives
    )


    # ======================================================
    # Observer
    # ======================================================

    observer = Observer(
        radius = observer_radius
    )


    # ======================================================
    # Accretion Disk
    # ======================================================

    disk = AccretionDisk(
        inner_radius=3.0,
        outer_radius=8.0,
        brightness=255
    )

    # ======================================================
    # Star Field
    # ======================================================

    star_field = StarField(
        "assets/milky_way.jpg"
    )

    # ======================================================
    # Scene
    # ======================================================

    scene = Scene(
        black_hole=bh,
        observer=observer,
        star_field=star_field,
        accretion_disk=disk
    )


    # ======================================================
    # Camera
    # ======================================================

    camera = Camera(
        observer=observer,
        width=settings.width,      # Increase later
        height=settings.height,
        fov=settings.fov
    )

    # ======================================================
    # Ray Generator
    # ======================================================

    generator = KerrRayGenerator(
        metric
    )

    #======================================================
    # Renderer
    # ======================================================

    tracer = KerrRayTracer(
        scene,
        camera,
        generator,
        simulator,
        settings
    )


    # ======================================================
    # Render
    # ======================================================
    direction = np.array([1.0, 0.0, 0.0])


    image = tracer.render()

    filename = "backend/static/render.png"

    plt.imsave(
        filename,
        np.clip(image / 255.0, 0, 1)
    )

    return filename
