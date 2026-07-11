stella_nova/
│
├── app.py          ✅
├── README.md
├── requirements.txt
├── phase1_demo_black_hole.py          ✅
├── metric_demo.py          ✅
├── geodesic_demo.py          ✅
├── christoffel_demo.py          ✅
├── orbit_demo.py          ✅
├── orbital_geodesics.py          ✅
├── radial_infall_demo.py          ✅
├── validation_demo.py          ✅
├── escape_trajectory_demo.py          ✅
├── effective_potential_demo.py          ✅
├── elliptical_orbit_demo.py          ✅
├── multiple_particle_demo.py          ✅
├── orbit_classification_demo.py          ✅
│
├── models/
│   ├── __init__.py          ✅
│   ├── black_hole.py          ✅
│   ├── photon.py
│   ├── particle.py
│   ├── accretion_disk.py
│   ├── observer.py
│   ├── camera.py
│   ├── star_field.py
│   └── scene.py
│
├── physics/
│   ├── geodesics.py          ✅
│   ├── integrator.py          ✅
│   ├── metrics.py          ✅
│   ├── christoffel.py          ✅
│   ├── initial_conditions.py          ✅
│   ├── integrator.py          ✅
│   ├── orbit_simulator.py          ✅
│   ├── orbit_classifier.py          ✅
│   ├── particle_ensemble.py          ✅
│   ├── #particle_initial_condition.py          ✅
│   ├── energy.py          ✅
│   ├── angular_momentum.py          ✅
│   ├── effective_potential.py          ✅
│   ├── photon.py          ✅
│   ├── validation/
│   │   ├── energy drift          ✅
│   │   ├── angular momentum drfit          ✅
│   │   ├── integration error
│   │   ├── step size          ✅
│   │   └── runtime          ✅
│   ├── units.py
│   ├── constants.py          ✅
│   └── radial_infall_simulation.py          ✅
│
├── renderer/
│   ├── raytracer.py
│   ├── shaders.py
│   ├── camera.py
│   ├── intersection.py
│   ├── background.py
│   ├── renderer.py
│   ├── image.py
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

Phase 2: Particle Dynamics                       🚧
---------------------------------------------------------
✓ Circular Orbit
✓ Radial Infall
✓ Escape Trajectory
✓ Engine Validation (Energy + Angular Momentum)
✓ Elliptical Orbit
✓ Photon Initial Conditions
⬜ Orbit Classification
✓ Effective Potential
✓ Multiple Particle Simulation

Phase 3: Photon Ray Tracing
---------------------------------------------------------
✓ Photon Initial Conditions
⬜ Null Geodesics
✓ Light Bending
⬜ Einstein Ring
⬜ Photon Sphere
✓ Radial Photon

Phase 4: Rendering
---------------------------------------------------------
✓ Observer
✓ Camera
⬜ StarField
⬜ AccretionDisk
⬜ Schwarzschild Ray Tracer
✓ Ray Generation
⬜ Image Plane

Phase 5: Kerr Black Hole
---------------------------------------------------------
⬜ KerrBlackHole
⬜ Frame Dragging
⬜ Kerr Photon Orbits

Phase 6: Website
---------------------------------------------------------
⬜ Interactive Controls
⬜ Real-time Simulation
⬜ Dashboard
⬜ Final Competition Version




what is step_size
what is step