import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np

from models.black_hole import BlackHole
from models.observer import Observer

from physics.kerr_metric import KerrMetric
from physics.kerr_observer_tetrad import KerrObserverTetrad

bh = BlackHole(
    mass=1,
    spin=0.9
)

metric = KerrMetric(bh)

observer = Observer(
    radius=10,
    theta=np.pi/2
)

tetrad = KerrObserverTetrad(metric)

basis = tetrad.basis(observer)

for name, vec in basis.items():

    print("--------------------------------")
    print(name)
    print(vec)