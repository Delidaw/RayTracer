import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from rendering.render_config import RenderConfig

config = RenderConfig()

print("Resolution :", config.width, "x", config.height)
print("FOV        :", config.fov)
print("Step Size  :", config.step_size)
print("Steps      :", config.steps)