import numpy as np

from models.black_hole import BlackHole
from physics.kerr_derivatives import KerrDerivatives
from physics.kerr_metric import KerrMetric

bh = BlackHole(mass = 1.0, spin = 0.5)

metric = KerrMetric(bh)

derivatives = KerrDerivatives(metric)

derivatives.compute(10, np.pi / 2)