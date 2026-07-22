import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np

from models.black_hole import BlackHole
from physics.kerr_metric import KerrMetric
from physics.kerr_observer_tetrad import KerrObserverTetrad

bh = BlackHole(
    mass=1,
    spin=0.9
)

metric = KerrMetric(bh)

tetrad = KerrObserverTetrad(metric)

r = 10
theta = np.pi/2

print("alpha =", tetrad.alpha(r, theta))
print()
print("e_t =")
print(tetrad.e_t(r, theta))