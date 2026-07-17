import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.black_hole import BlackHole
from physics.impact_parameter import ImpactParameter


#-----------------------------
#Create BlackHole
#-----------------------------

black_hole = BlackHole(mass = 1.0)

impact = ImpactParameter(black_hole)

#----------------------------
#Critical Impact Parameter
#----------------------------

bc = impact.critical()

print("=" * 50)
print("Impact Parameter Validation")
print("=" * 50)

print(f"Mass M = {black_hole.mass}")
print(f"Critical Impact Parameter = {bc:.10f}")
print()

#----------------------------
#Classification Tests
#----------------------------

tests = [
    bc - 0.1,
    bc,
    bc + 0.1
]

for b in tests:

    print(f"Impact Parameter = {b:.6f}")

    print(
        "Classification: ",
        impact.classify(b)
    )

    print()