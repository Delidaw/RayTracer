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
theta = np.pi / 2

print("g_tt =", tetrad.g_tt(r, theta))
print("g_tphi =", tetrad.g_tphi(r, theta))
print("g_rr =", tetrad.g_rr(r, theta))
print("g_thetatheta =", tetrad.g_thetatheta(r, theta))
print("g_phiphi =", tetrad.g_phiphi(r, theta))