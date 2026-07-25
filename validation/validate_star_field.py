import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.star_field import StarField
import numpy as np

stars = StarField()

print(stars.sample(np.array([0,0,1])))