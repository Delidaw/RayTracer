import numpy as np

from models.black_hole import BlackHole
from physics.kerr_metric import KerrMetric

bh = BlackHole(mass = 1.0, spin = 0.5)

metric = KerrMetric(bh)

r = 10
theta = np.pi / 2

g = metric.metric_tensor(r, theta)

print("Sigma = ", metric.sigma(r, theta))

print("Delta = ", metric.delta(r))

print("g =", g)