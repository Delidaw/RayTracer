import numpy as np

from models.black_hole import BlackHole
from physics.schwarzschild_metric import SchwarzschildMetric
from physics.kerr_metric import KerrMetric

# Same black hole parameters
mass = 1.0

# Schwarzschild black hole
bh_s = BlackHole(mass=mass)

# Kerr black hole with zero spin
bh_k = BlackHole(mass=mass, spin=0.0)

schwarzschild = SchwarzschildMetric(bh_s)
kerr = KerrMetric(bh_k)

r = 20
theta = np.pi / 2

g_s = schwarzschild.metric_tensor(r, theta)
g_k = kerr.metric_tensor(r, theta)

print("\n==========================")
print("SCHWARZSCHILD METRIC")
print("==========================")
print(g_s)

print("\n==========================")
print("KERR METRIC (a = 0)")
print("==========================")
print(g_k)

print("\n==========================")
print("DIFFERENCE")
print("==========================")
print(g_s - g_k)