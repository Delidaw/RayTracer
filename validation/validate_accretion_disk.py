import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.accretion_disk import AccretionDisk

disk = AccretionDisk(
    inner_radius=3,
    outer_radius=8
)

print(disk.contains(2))
print(disk.contains(5))
print(disk.contains(10))