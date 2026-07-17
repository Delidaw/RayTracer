stella_nova/
│
├── app.py                               ✅
├── README.md
├── requirements.txt
├── phase1_demo_black_hole.py            ✅
├── metric_demo.py                       ✅
├── geodesic_demo.py                     ✅
├── christoffel_demo.py                  ✅
├── orbit_demo.py                        ✅
├── orbital_geodesics.py                 ✅
├── radial_infall_demo.py                ✅
├── validation_demo.py                   ✅
├── escape_trajectory_demo.py            ✅
├── effective_potential_demo.py          ✅
├── elliptical_orbit_demo.py             ✅
├── multiple_particle_demo.py            ✅
├── orbit_classification_demo.py         ✅
├── photon_radial_demo.py                ✅
├── photon_null_validation.py            ✅
├── light_bending_demo.py                ✅
├── ray_tracer_demo.py
│
├── models/
│   ├── __init__.py                      ✅
│   ├── black_hole.py                    ✅
│   ├── photon.py
│   ├── particle.py
│   ├── accretion_disk.py
│   ├── observer.py                      ✅
│   ├── camera.py                        ✅
│   ├── star_field.py
│   └── scene.py
│
├── physics/
│   ├── geodesics.py                     ✅
│   ├── integrator.py                    ✅
│   ├── metrics.py                       ✅
│   ├── christoffel.py                   ✅
│   ├── initial_conditions.py            ✅
│   ├── integrator.py                    ✅
│   ├── orbit_simulator.py               ✅
│   ├── orbit_classifier.py              ✅
│   ├── particle_ensemble.py             ✅
│   ├── #particle_initial_condition.py   ✅
│   ├── energy.py                        ✅
│   ├── angular_momentum.py              ✅
│   ├── effective_potential.py           ✅
│   ├── photon.py                        ✅
│   ├── ray_generator.py                 ✅
│   ├── ray_physics.py                   ✅
│   ├── observer_tetrad.py               ✅
│   ├── null_photon.py                   ✅
│   ├── photon_initial_conditions.py     ✅
│   ├── validation/
│   │   ├── energy drift                 ✅
│   │   ├── angular momentum drfit       ✅
│   │   ├── integration error
│   │   ├── step size                    ✅
│   │   └── runtime                      ✅
│   ├── units.py
│   ├── constants.py                     ✅
│   └── radial_infall_simulation.py      ✅
│
├── rendering/
│   ├── raytracer.py                     ✅
│   ├── shaders.py                     ✅
│   ├── observer.py                      ✅
│   ├── observer_tetrad.py               ✅
│   ├── star_field.py                    ✅
│   ├── ray_physics.py                   ✅
│   ├── camera.py                     ✅
│   ├── intersection.py
│   ├── background.py
│   ├── renderer.py
│   ├── image_plane.py
│   └── textures.py
│
├── pages/
│   ├── home.py          ✅
│   ├── renderer_page.py          ✅
│   ├── photon path.py          ✅
│   ├── curvature mesh.py          ✅
│   ├── lensing.py          ✅
│   ├── ray animation.py          ✅
│   ├── deflection.py          ✅
│   ├── intensity.py          ✅
│   ├── orbits.py          ✅
│   ├── plots.py
│   ├── chatbot          ✅
│   └── newton vs genral relativity.py          ✅
│
├── assets/
│
├── utils/
│   ├── plotting.py
│   ├── units.py
│   ├── logger.py
│   └── helpers.py
│
├── docs/
│
├── theory.pdf
│
├── equations.pdf
│
├── algorithm.pdf
│
└── tests/






Phase 1: Schwarzschild Engine                    ✅ COMPLETE
---------------------------------------------------------
✓ BlackHole
✓ Schwarzschild Metric
✓ Christoffel Symbols
✓ Geodesic Equation
✓ RK4 Integrator
✓ Orbit Simulator
✓ Validation (basic)

Phase 2: Particle Dynamics                       
---------------------------------------------------------
✓ Circular Orbit
✓ Radial Infall
✓ Escape Trajectory
✓ Engine Validation (Energy + Angular Momentum)
✓ Elliptical Orbit
✓ Photon Initial Conditions
✓ Orbit Classification
✓ Effective Potential
✓ Energy Conservation
✓ Angular Momentum Conservation
✓ Multiple Particle Simulation

Phase 3: Photon Ray Tracing
---------------------------------------------------------
✓ Photon Initial Conditions
✓ Null Geodesics
✓ Light Bending
⬜ Einstein Ring      4
⬜ Photon Sphere      3
✓ Radial Photon
✓ Proper Null Four-Momentum
⬜ Impact Parameter Validation
✅ Tetrad Transformation
⬜ Escape/Capture Detection    1

Phase 4: Rendering
---------------------------------------------------------
✓ Observer
✓ Camera
✓ StarField
✓ Local Orthonormal Tetrad
✓ Rendering Loop
⬜ AccretionDisk     5
⬜ Schwarzschild Ray Tracer
✓ Ray Generation
⬜ Image Plane
✓ Ray Physics
⬜ Black Hole Shadow        2
⬜ Background Texture
⬜ Redshift Coloring
⬜ Anti-aliasing

Phase 5: Kerr Black Hole
---------------------------------------------------------
⬜ KerrBlackHole
⬜ Frame Dragging
⬜ Kerr Photon Orbits
⬜ Kerr Metric
⬜ Kerr Christoffels
⬜ Kerr Ray Tracer
⬜ Rotating Shadow

Phase 6: Website
---------------------------------------------------------
⬜ Interactive Controls
⬜ Real-time Simulation
⬜ Dashboard
⬜ Final Competition Version
⬜ Simulation Dashboard
⬜ Live Parameter Sliders
⬜ Image Renderer
⬜ Educational Mode
⬜ Competition Version

Phase 7: Optimization
---------------------------------------------------------
⬜ Adaptive RK4
⬜ Parallel Ray Tracing
⬜ NumPy Optimization
⬜ Numba
⬜ Multi-core Rendering
⬜ Image Caching

Phase 8: Research Features
---------------------------------------------------------
⬜ Validation against EinsteinPy
⬜ Comparison with Newtonian Gravity
⬜ Numerical Error Analysis
⬜ Performance Benchmarks
⬜ Physical Accuracy Tests
⬜ Research Paper Figures


renderer pipeline

Observer
      │
      ▼
Camera
      │
      ▼
Pixel Grid
      │
      ▼
Ray Directions
      │
      ▼
RayGenerator   ← (this file)
      │
      ▼
OrbitSimulator
      │
      ▼
Photon Trajectory
      │
      ▼
Hit? Escape? Disk?
      │
      ▼
Pixel Color
      │
      ▼
Final Black Hole Image


Finish the star field sampling (replace the gradient with stars).
Fix the escape/capture logic so rays that hit the event horizon become black.
Add the accretion disk.
Implement the Einstein ring.
Optimize the renderer (parallelism/vectorization).
Increase to high resolution (e.g. 800×800 or 1000×1000).




✓ BlackHole
✓ Schwarzschild Metric
✓ Christoffel Symbols
✓ Geodesic Equation
✓ RK4 Integrator
✓ Orbit Simulator
✓ Validation (basic)
✓ Circular Orbit
✓ Radial Infall
✓ Escape Trajectory
✓ Engine Validation (Energy + Angular Momentum)
✓ Elliptical Orbit
✓ Photon Initial Conditions
✓ Effective Potential
✓ Multiple Particle Simulation
✓ Photon Initial Conditions
✓ Null Geodesics
✓ Light Bending
✓ Radial Photon
✓ Observer
✓ Camera
✓ StarField
✓ Local Orthonormal Tetrad
✓ Rendering Loop
✓ Ray Generation
✓ Ray Physics


TO DO
✅ Fix photon launch (proper null four-vector)
✅ Correct black-hole shadow
✅ Escape vs capture classification
✅ Einstein ring
✅ Accretion disk
✅ Performance optimization
✅ Website integration
✅ Kerr spacetime




✅ Schwarzschild metric
✅ Christoffel symbol computation
✅ RK4 geodesic integrator
✅ Photon initial conditions
✅ Observer tetrad
✅ Ray generation
✅ Camera model
✅ Ray tracer
✅ Star field rendering
✅ Orbit classification
✅ Effective potential
✅ Validation tests
✅ Multiple demos




Phase 5 Roadmap

This is what I recommend.

Phase 5.1

Metric abstraction

Current:

physics/
    schwarzschild_metric.py

We'll create

physics/

metric.py
schwarzschild_metric.py
kerr_metric.py

where

Metric

is a base class.

Everything else will work with

Metric

instead of specifically

SchwarzschildMetric
Phase 5.2

Implement Kerr metric

This is purely mathematics.

We'll code

g
μν
	​


in Boyer-Lindquist coordinates.

Inputs

M
a
r
θ

Outputs

g_tt
g_rr
g_θθ
g_φφ
g_tφ

Notice that unlike Schwarzschild,

there are now off-diagonal terms

g
tϕ
	​


which represent frame dragging.

Phase 5.3

Inverse metric

Compute

g
μν

This is needed for Christoffel symbols.

Phase 5.4

Christoffel symbols

Your current Christoffel code should mostly remain unchanged.

It only needs the metric and its derivatives.

If we wrote it generically,

Kerr should "just work."

Phase 5.5

Photon geodesics

Now integrate

t
r
θ
φ

instead of assuming Schwarzschild symmetry.

Unlike Schwarzschild,

photons

spiral
precess
get frame dragged
Phase 5.6

Black hole shadow

This is the exciting part.

Instead of

○

your shadow becomes

◔

shifted to one side because of rotation.

Phase 5.7

Accretion disk

Now we add

==============
      ◯
==============

Around Kerr,

one side becomes brighter because of

Doppler boosting
relativistic beaming
Phase 5.8

Frame dragging visualization

One of my favorite demos.

Show nearby particles.

Without spin:

↓

↓

↓

↓


With spin:

↺
↺
↺
↺

Everything gets dragged around the black hole.

Phase 5.9

Ergosphere

Unlike Schwarzschild,

Kerr has

event horizon
ergosphere

Visualize both.

The ergosphere looks like

   ______
 /        \
|          |
|   ____   |
|  /    \  |
 \________/

where the outer boundary is the ergosphere and the inner one is the event horizon.

New folder structure

Eventually I'd like Stella Nova to look something like

physics/

metric.py
schwarzschild_metric.py
kerr_metric.py

christoffel.py
integrator.py
geodesics.py

observer_tetrad.py
ray_generator.py

rendering/

schwarzschild_ray_tracer.py
kerr_ray_tracer.py

validation/

kerr_metric_validation.py
frame_dragging_validation.py






what is step_size
what is step





