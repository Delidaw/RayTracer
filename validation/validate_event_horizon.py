import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.black_hole import BlackHole
from physics.event_horizon import EventHorizon

bh = BlackHole(
    mass=1,
    spin=0.9
)

horizon = EventHorizon(bh)

print("Event Horizon Radius")
print("---------------------")
print(horizon.radius())