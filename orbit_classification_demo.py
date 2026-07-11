import numpy as np
import matplotlib.pyplot as plt

from models.black_hole import BlackHole

from physics.initial_conditions import InitialConditions
from physics.orbit_simulator import OrbitSimulator
from physics.orbit_classifier import OrbitClassifier

bh = BlackHole(mass = 1)

initial = InitialConditions(bh)

simulator = OrbitSimulator(bh)

classifier = OrbitClassifier(bh)

#       initial.escape_trajectory(
#           radius = 20,
#           radial_velocity = -0.2,
#           angular_velocity = 0.0
#        ),

trajectory = simulator.simulate(
    initial.radial_infall(radius=20),
    step_size=0.01,
    steps=30000
)

print("\nRadial Infall")
print(classifier.classify(trajectory))


"""
trajectory = simulator.simulate(
    initial.circular_orbit(radius=10),
    step_size=0.01,
    steps=30000
)

print("\nCircular Orbit")
print(classifier.classify(trajectory))
"""

"""
trajectory = simulator.simulate(
    initial.elliptical_orbit(
        semi_major_axis=20,
        eccentricity=0.4
    ),
    step_size=0.01,
    steps=50000
)

print("\nElliptical Orbit")
print(classifier.classify(trajectory))
"""

"""
trajectory = simulator.simulate(
    initial.escape_trajectory(
        radius=20,
        radial_velocity=0.2,
        angular_velocity=0.02
    ),
    step_size=0.01,
    steps=30000
)

print("\nEscape Trajectory")
print(classifier.classify(trajectory))
"""