PHOTON FORGE GPU RENDERER V2

This is a new modular WebGL2 renderer. It keeps the existing Python engine untouched.

FILES
-----
backend/templates/hybrid_renderer_v2.html
backend/static/gpu-v2/style.css
backend/static/gpu-v2/renderer.js
ROUTES_PATCH.txt

INSTALL
-------
1. Copy the backend/templates and backend/static folders into your Photon Forge project.
   Merge them with the existing folders; do not delete your current files.

2. Add the route from ROUTES_PATCH.txt to backend/routes.py.

3. From the project root run:
   python -m backend.app

4. Open:
   http://127.0.0.1:5000/renderer-v2

WHAT THIS VERSION IMPLEMENTS
----------------------------
- Realtime WebGL2 rendering
- Curvature-adaptive GPU ray stepping
- Kerr-inspired frame-dragging preview term
- Volumetric accretion flow instead of a flat disk-plane hit
- Emission/absorption radiative-transfer approximation
- Temperature colours:
  below 4000 K red
  4000–5500 K orange
  5500–7000 K white
  7000–9500 K cyan
  above 9500 K blue
- Relativistic Doppler beaming approximation
- Gravitational redshift approximation
- Procedural lensed star background
- ACES-style tone mapping
- Performance, Balanced, Quality and Ultra presets
- URL hash state such as #zoom=18&preset=balanced
- Mouse orbit, wheel zoom and fullscreen

IMPORTANT SCIENTIFIC NOTE
-------------------------
The Python renderer remains the validated reference engine.
This GPU renderer is the interactive implementation and currently uses a Kerr-inspired numerical approximation rather than a line-for-line port of the full Python geodesic equations.

The next scientific milestone is to port the exact photon state derivative used by your Python Kerr engine and validate selected GPU rays against Python trajectories.
