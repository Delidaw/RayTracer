import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.black_hole import BlackHole
from physics.kerr_isco import KerrISCO

for spin in [0.0, 0.3, 0.6, 0.9, 0.99]:

    bh = BlackHole(
        mass=1,
        spin=spin
    )

    isco = KerrISCO(bh)

    print("-------------------------")
    print("a =", spin)
    print("Prograde :", isco.prograde())
    print("Retrograde:", isco.retrograde())