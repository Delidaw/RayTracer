import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from physics.adaptive_rk4 import AdaptiveRK4


adaptive = AdaptiveRK4()

print()
print("=" * 60)
print("ADAPTIVE RK4 VALIDATION")
print("=" * 60)

radii = [
    1.5,
    2.0,
    2.5,
    3.0,
    5.0,
    10.0,
    20.0,
    50.0,
    100.0,
]

for r in radii:

    h = adaptive.step_size(r)

    print(
        f"r = {r:6.2f}   step size = {h:.5f}"
    )

print()
print("=" * 60)
print("VALIDATION COMPLETE")
print("=" * 60)