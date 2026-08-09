# rendering/render_settings.py

from dataclasses import dataclass


@dataclass
class RenderSettings:
    """
    Global rendering settings for Photon Forge.

    A single RenderSettings object controls the quality,
    performance, and visual effects of a render.
    """

    # --------------------------------------------------
    # Image
    # --------------------------------------------------

    width: int = 10
    height: int = 10
    fov: float = 60.0

    # --------------------------------------------------
    # Ray tracing
    # --------------------------------------------------

    steps: int = 20
    step_size: float = 0.05

    # --------------------------------------------------
    # Rendering
    # --------------------------------------------------

    exposure: float = 1.0

    bloom: bool = True
    blur: bool = True

    # --------------------------------------------------
    # Performance
    # --------------------------------------------------

    adaptive_sampling: bool = True

    max_workers: int | None = None

    # --------------------------------------------------
    # Output
    # --------------------------------------------------

    save_image: bool = False

    output_directory: str = "renders"