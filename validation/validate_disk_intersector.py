import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np

from models.accretion_disk import AccretionDisk
from rendering.disk_intersector import DiskIntersector

disk = AccretionDisk(
    inner_radius=3,
    outer_radius=8
)

intersector = DiskIntersector(disk)

print("=== Should intersect ===")

trajectory_hit = np.array([
    [0,20,np.pi/2,0,0,0,0,0],
    [0,10,np.pi/2,0,0,0,0,0],
    [0, 6,np.pi/2,0,0,0,0,0],   # Inside disk
    [0, 2,np.pi/2,0,0,0,0,0],
])

hit, state = intersector.intersects(
    trajectory_hit
)

print(hit)
print(state)


print("\n=== Should miss ===")

trajectory_miss = np.array([
    [0,20,np.pi/2,0,0,0,0,0],
    [0,10,np.pi/2,0,0,0,0,0],
    [0, 9,np.pi/2,0,0,0,0,0],   # Outside disk
])

hit, state = intersector.intersects(
    trajectory_miss
)

print(hit)
print(state)