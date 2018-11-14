#!/usr/bin/env python3

import os, time
import numpy as np
from util import load, save
from model import Model, Pair, RULES, STATES

# # load models
# path = os.path.abspath(os.path.join(os.path.dirname(__file__), "models.pkl"))
# baseline, models = load(path)

# # reformat as 16-dimensional points
# matrices = [model.rules for model in models]
# points = []
# for matrix in matrices:
# 	point = []
# 	for state_1 in STATES:
# 		for state_2 in STATES:
# 			point.append(matrix[state_1][state_2])
# 	points.append(point)
# points = np.array(points)

# save("points.pkl", points)

points = load("points.pkl")
print(points)

