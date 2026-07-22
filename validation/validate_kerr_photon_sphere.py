import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.black_hole import BlackHole
from physics.kerr_photon_sphere import KerrPhotonSphere

for spin in [0.0, 0.3, 0.6, 0.9, 0.99]:

    bh = BlackHole(
        mass = 1,
        spin = spin
    )

    sphere = KerrPhotonSphere(bh)

    print("--------------------------")
    print(f"a = {spin}")
    print("Prograde :", sphere.prograde())
    print("Retrograde : ", sphere.retrograde())